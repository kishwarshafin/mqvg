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

echo converting gam to json
vg view -a $input > $file.json
echo converting json to mqvg input file
python3 jsonParser.py < $file.json >$output/vg_predict
rm $file.json
echo process finished

