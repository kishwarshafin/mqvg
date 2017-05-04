#!/bin/bash
input=inputs
mkdir $input

if [ ! -e $input/Test_human_10K ];
then
    echo downloading test file
    wget https://users.soe.ucsc.edu/~shafin/files/human_10K/Test_human_10K -P $input/
fi

if [ ! -e $input/Train_human_10K ];
then
    echo downloading training file
    wget https://users.soe.ucsc.edu/~shafin/files/human_10K/Train_human_10K -P $input/
fi

if [ ! -e $input/Predict_human_10K ];
then
    echo downloading prediction file
    wget https://users.soe.ucsc.edu/~shafin/files/human_10K/Predict_human_10K -P $input/
fi

python3 logisticRegression.py --model_dir="./runDir" --train_step=2000 --train_data="./inputs/Train_human_10K" --test_data="./inputs/Test_human_10K" --predict_data="./inputs/Predict_human_10K"
