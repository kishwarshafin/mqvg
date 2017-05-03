from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import argparse
import sys
import os
import pandas as pd
import tensorflow as tf
from datetime import datetime

COLUMNS = ["name", "mapping_quality", "best_score", "mapped_state"]
PREDICT_COLUMNS = ["name", "mapping_quality", "best_score", "mapped_state"]
LABEL_COLUMN = "mapped_state"
CONTINUOUS_COLUMNS = ["mapping_quality", "best_score"]

class TextColor:
    """
    Defines color codes for text used to give different mode of errors.
    """
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class LogisticRegression:
    def setTrainData(self, trainDataFrame, trainSteps):
        self.trainDataFrame = trainDataFrame
        self.trainSteps = trainSteps

    def setTestData(self, testDataFrame):
        self.testDataFrame = testDataFrame

    def setPredictData(self, predictDataFrame):
        self.predictDataFrame = predictDataFrame

    def createEstimator(self, learningRate, l1regularization_strength, l2regularization_strength, modelDirectory):
        print("Learning Rate: ",learningRate,l1regularization_strength, l2regularization_strength)
        mapping_quality = tf.contrib.layers.real_valued_column("mapping_quality")
        best_score = tf.contrib.layers.real_valued_column("best_score")
        wide_columns = [mapping_quality, best_score]
        self.model = tf.contrib.learn.LinearClassifier(feature_columns=wide_columns,
                                              optimizer=tf.train.FtrlOptimizer(learning_rate=learningRate,
                                                                               l1_regularization_strength=l1regularization_strength,
                                                                               l2_regularization_strength=l2regularization_strength),
                                              model_dir=modelDirectory)

    def input_fn(self,df):
        continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
        feature_cols = dict(continuous_cols)
        label = tf.constant(df[LABEL_COLUMN].values)
        return feature_cols, label

    def Train_Model(self):
        self.model.fit(input_fn=lambda: self.input_fn(self.trainDataFrame), steps=self.trainSteps)

    def Evaluate_Model(self):
        evaluationResult = self.model.evaluate(input_fn=lambda: self.input_fn(self.testDataFrame), steps=1)
        for key in sorted(evaluationResult):
            print("%s: %s" % (key, evaluationResult[key]))

    def Predict_Using_TrainedModel(self, outputDirectory, outputFile):
        predictions = list(self.model.predict_proba(input_fn =lambda: self.input_fn(self.predictDataFrame), as_iterable=True))
        index = 0
        try:
            os.stat(outputDirectory)
        except:
            os.mkdir(outputDirectory)

        with open(outputDirectory+"/"+outputFile, 'w') as f:
            for idx, row in self.predictDataFrame.iterrows():
                if float(predictions[index][1]) > 0.0000000001:
                    p = np.log10(float(predictions[index][1]))
                else:
                    p = 0
                qValue = int(-10 * int(p))
                if row[PREDICT_COLUMNS[3]]:
                    print(row[PREDICT_COLUMNS[0]], "\t", row[PREDICT_COLUMNS[1]], "\t",row[PREDICT_COLUMNS[2]], "\t", qValue,"\t", row[PREDICT_COLUMNS[3]], file=f)
                else:
                    print(row[PREDICT_COLUMNS[0]], "\t", row[PREDICT_COLUMNS[1]], "\t", row[PREDICT_COLUMNS[2]], "\t", qValue,"\t", "0", file=f)
                index += 1

class IO_handler:
    def _GetDataFrame_(self, file_name, columns, engine, separator, dropFlag=1):
        df = pd.read_csv(
            tf.gfile.Open(file_name),
            names=columns,
            engine=engine,
            sep=separator)

        df = df.dropna(how='any', axis=0)
        return df

    def Train(self, regressionObject):
        regressionObject.Train_Model()

    def ControllerMethod(self):
        sys.stderr.write(TextColor.GREEN + "INFO: READING DATA FRAMES\n" + TextColor.END)
        train, test, predict = (0,0,0)
        self.modelDirectory = FLAGS.model_dir
        if FLAGS.train_data:
            if not os.path.isfile(FLAGS.train_data):
                parser.print_help()
                sys.stderr.write(TextColor.RED+"ERROR: "+FLAGS.train_data+" FILE NOT FOUND\n"+TextColor.END)
                raise FileNotFoundError
            self.trainDataFrame = self._GetDataFrame_(FLAGS.train_data, COLUMNS, "python", "\t")
            self.trainDataFrame[LABEL_COLUMN] = self.trainDataFrame["mapped_state"]
            self.trainSteps = FLAGS.train_steps
            train = 1
        if FLAGS.test_data:
            if not os.path.isfile(FLAGS.test_data):
                parser.print_help()
                sys.stderr.write(TextColor.RED + "ERROR: " + FLAGS.test_data + " FILE NOT FOUND\n"+TextColor.END)
                raise FileNotFoundError
            self.testDataFrame = self._GetDataFrame_(FLAGS.test_data, COLUMNS, "python", "\t")
            self.testDataFrame[LABEL_COLUMN] = self.testDataFrame["mapped_state"]
            test = 1
        if FLAGS.predict_data:
            if not os.path.isfile(FLAGS.predict_data):
                parser.print_help()
                sys.stderr.write(TextColor.RED + "ERROR: " + FLAGS.predict_data + " FILE NOT FOUND"+TextColor.END)
                raise FileNotFoundError
            self.predictDataFrame = self._GetDataFrame_(FLAGS.predict_data, PREDICT_COLUMNS, "python", "\t", 0)
            self.outputFileName = FLAGS.output_file
            self.outputDirectory = FLAGS.output_dir
            predict = 1
        regressionObject = LogisticRegression()
        regressionObject.createEstimator(FLAGS.learning_rate, FLAGS.l1_regularization_rate, FLAGS.l2_regularization_rate, self.modelDirectory)
        if train:
            sys.stderr.write(TextColor.GREEN+"INFO: TRAINING THE MODEL\n"+TextColor.END)
            regressionObject.setTrainData(self.trainDataFrame, self.trainSteps)
            regressionObject.Train_Model()
            sys.stderr.write(TextColor.GREEN+"INFO: TRAINING FINISHED\n"+TextColor.END)
        if test:
            sys.stderr.write(TextColor.GREEN+"INFO: EVALUATING THE MODEL\n"+TextColor.END)
            regressionObject.setTestData(self.testDataFrame)
            regressionObject.Evaluate_Model()
            sys.stderr.write(TextColor.GREEN+"INFO: EVALUATION FINISHED\n"+TextColor.END)
        if predict:
            sys.stderr.write(TextColor.GREEN+"INFO: PREDICTING BASED ON TRAINED MODEL"+TextColor.END)
            regressionObject.setPredictData(self.predictDataFrame)
            regressionObject.Predict_Using_TrainedModel(self.outputDirectory, self.outputFileName)
            sys.stderr.write(TextColor.GREEN+"INFO: PREDICTION FINISHED \n"+TextColor.END)
            sys.stderr.write(TextColor.GREEN + "INFO: OUTPUT SAVED IN: "+self.outputDirectory+self.outputFileName+"\n" + TextColor.END)




FLAGS = None
parser = None

def main(_):
    tf.logging.set_verbosity(tf.logging.ERROR)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    ioObject = IO_handler()
    ioObject.ControllerMethod()

def checkModelDir():
    try:
        os.stat(FLAGS.model_dir)
    except:
        sys.stderr.write(TextColor.YELLOW + "Model directory not found\n" + TextColor.END)
        sys.stderr.write(TextColor.YELLOW + "Creating directory"+ str(FLAGS.model_dir)+ "\n" + TextColor.END)
        os.mkdir(FLAGS.model_dir)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.register("type", "bool", lambda v: v.lower() == "true")
  parser.add_argument(
      "--model_dir",
      type=str,
      default="./modelDir",
      help="Base directory for output models."
  )
  parser.add_argument(
      "--train_steps",
      type=int,
      default=100,
      help="Number of training steps."
  )
  parser.add_argument(
      "--train_data",
      type=str,
      help="Path to the training data."
  )
  parser.add_argument(
      "--test_data",
      type=str,
      help="Path to the test data."
  )
  parser.add_argument(
      "--predict_data",
      type=str,
      help="Path to the prediction data."
  )
  parser.add_argument(
      "--output_dir",
      type=str,
      default="./output",
      help="Path to the prediction data."
  )
  parser.add_argument(
      "--output_file",
      type=str,
      default="output"+str(datetime.now()).replace(' ','')+".txt",
      help="Path to the prediction data."
  )
  parser.add_argument(
      "--learning_rate",
      type=float,
      default=0.1,
      help="Learning rate of the model."
  )
  parser.add_argument(
      "--l1_regularization_rate",
      type=float,
      default=1.0,
      help="L1 Regularization rate"
  )
  parser.add_argument(
      "--l2_regularization_rate",
      type=float,
      default=1.0,
      help="L2 Regularization rate"
  )
  FLAGS, unparsed = parser.parse_known_args()
  checkModelDir()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)

