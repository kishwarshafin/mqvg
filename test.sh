#!/bin/bash
input=inputs
mkdir $input

if [ ! -e $input/vg_human_test ];
then
    echo downloading test file
    wget https://users.soe.ucsc.edu/~shafin/files/hg_human/vg_human_test -P $input/
fi

if [ ! -e $input/vg_human_train ];
then
    echo downloading training file
    wget https://users.soe.ucsc.edu/~shafin/files/hg_human/vg_human_train -P $input/
fi

if [ ! -e $input/vg_human_predict ];
then
    echo downloading prediction file
    wget https://users.soe.ucsc.edu/~shafin/files/hg_human/vg_human_predict -P $input/
fi

python3 logisticRegression.py --model_dir="./runDir" --train_step=200 --train_data="./inputs/vg_human_train" --test_data="./inputs/vg_human_test" --predict_data="./inputs/vg_human_predict"
