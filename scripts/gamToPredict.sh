#!/bin/bash

if [ $# -ne 2 ];
then
    echo "usage: "$(basename $0) "[gam-file]" "[output-dir]"
    echo "example: "$(basename $0) './inputs/sample' './inputs/'
    exit
fi

file=$1
input=$1.gam
output=$2
now=$(date '+%d%m%Y%H%M%S')

echo output will be $output/predict_file_$now
echo converting gam to json
vg view -a $input > $output/temp_json_$now.json

echo converting json to mqvg predict file
python3 jsonParser.py < $output/temp_json_$now.json >$output/predict_file_$now
rm $output/temp_json_$now.json
echo process finished

