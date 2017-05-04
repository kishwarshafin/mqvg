#!/bin/bash
input=inputs
mkdir $input

if [ ! -e $input/Test_human_2M ];
then
    echo downloading test file
    wget https://users.soe.ucsc.edu/~shafin/files/human_2M/Test_human_2M -P $input/
fi

if [ ! -e $input/Train_human_2M ];
then
    echo downloading training file
    wget https://users.soe.ucsc.edu/~shafin/files/human_2M/Train_human_2M -P $input/
fi

if [ ! -e $input/Predict_human_2M ];
then
    echo downloading prediction file
    wget https://users.soe.ucsc.edu/~shafin/files/human_2M/Predict_human_2M -P $input/
fi

python3 logisticRegression.py --model_dir="./runDir" --train_step=2000 --train_data="./inputs/Train_human_2M" --test_data="./inputs/Test_human_2M" --predict_data="./inputs/Predict_human_2M"

