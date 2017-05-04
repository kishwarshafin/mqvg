# MQVG

<i>MQVG</i> provides a calibration of mapping qualities provided by vg. This calibration can be used to better estimate the confidence of a mapped set to a reference variation graph. Primarily designed for human genome variation graph, this model can be used for other organisms too.

## Usage
-------
### Building
#### vg
To begin, you need to make sure you have [vg](https://github.com/vgteam/vg) installed in your system and it is available in your path. First install all the requirements. For linux based systems you can install the dependencies with apt-get.
```sh
sudo apt-get install build-essential git cmake pkg-config libncurses-dev libbz2-dev  \
                     protobuf-compiler libprotoc-dev libjansson-dev automake libtool \
                     jq bc rs curl unzip redland-utils librdf-dev bison flex
```

Then clone vg from git.
```sh
git clone --recursive https://github.com/vgteam/vg.git
cd /vg/
. ./source_me.sh && make static
```

You can run with ```./bin/vg``` but make sure vg command can be found in your path.<br/>
OSX users can use port or homebrew described in [vg documentation](https://github.com/vgteam/vg).
#### Python3 and Tensorflow
<i>MQVG</i> uses python 3.0+ and python libraries. Ubuntu 16.04 and later ships with python3. You can run ```python3 -V``` to check the version of python you are using.
```sh
sudo apt-get install python3
python3 -V
```
Then install Tensorflow and other required libraries:
```sh
sudo apt-get install python3-pip python3-dev
pip3 install tensorflow
pip3 install numpy
pip3 install scipy
pip3 install pandas
```
#### <i>MQVG</i>
After all the libraries are installed, clone <i>MQVG</i> and test.
```sh
git clone https://github.com/kishwarshafin/mqvg.git
```
Now you can test <i>MQVG</i> with some pre-compiled test and train data.
```sh
cd mqvg/scripts/
./testSmall.sh
```
## Testing, Training and Evaluation data model
-------
All dataset used for <i>MQVG</i> needs to be in a specific format. The gam converter files provided with <i>MQVG</i> can be used to convert vg produced gam files to train and test datasets.<br/>
#### Train Data
The train data follows the following format:

| Read Name        | Mapping Quality           | Score  | Mapped State  |
| ------------- |:-------------:| -----:| -----:|
| c4118d9b9bdbe99d0_1      | 60 | 89 | 1 |
| 122aaf7c7125a784_1      | 0 | 86 | 0 |

The training dataset can be built using data produced by ```vg sim``` and the script ```gamToTest.sh``` provided with <i>MQVG</i>.<br/>

When we run ```vg sim```, it produces a ```.compare``` file and a ```.gam``` file with the mapping information.

```sh
cd /mqvg/
./gamToTest.sh ~/inputs/sample-0_default ~/inputs/vg-0.compare ~/mqvg/inputs
```

This will produce a train file we can use for training the model.
#### Test/Evaluate Data
The test/evaluate data follows the exact same format of Test. What is generally followed is to shuffle extract 30% data from the test data and use that for testing/evaluation.

#### Predict Data
Predict data can exactly look like train data but it may follow the following format:

| Read Name        | Mapping Quality           | Score  |
| ------------- |:-------------:| -----:|
| c4118d9b9bdbe99d0_1      | 60 | 89 |
| 122aaf7c7125a784_1      | 0 | 86 |

In prediction dataset the mapped state whether the read is correctly mapped or not is missing as the model tries to predict that value.

To run prediction on a ```.gam``` file produced by ```vg map```, we can use the ```gamToPredict.sh``` script provided with <i>MQVG</i><br/>

```sh
cd /mqvg/scripts
./gamToPredict.sh ./inputs/sample ./inputs/
```

## <i>MQVG</i> Command line
-------
After generating testing and training data, we can run <i>MQVG</i>. A simple run can be:
```sh
python3 logisticRegression.py --model_dir="./runDir" --train_step=2000  --train_data="./inputs/train_1M" --test_data="./inputs/evaluate_2M" --predict_data="./inputs/predict_1M"
```

But we can change the parameters of the model for calibration: <br/>
* --model_dir :- Base directory to save checkpoints.
*  --train_steps :- Number of training steps.
*  --train_data :- Path to the training data.
*  --test_data :- Path to the test data.
*  --predict_data :- Path to the prediction data.
*  --output_dir :- Output directory.
*  --output_file :- Output file name.
*  --learning_rate :- Learning rate of the model. (0.1 is standard for human genome)
*  --l1_regularization_strength :- L1 Regularization strength
*  --l2_regularization_strength :- L2 Regularization strength
