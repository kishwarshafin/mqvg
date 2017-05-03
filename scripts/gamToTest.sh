#!/bin/bash

if [ $# -ne 3 ];
then
    echo "usage: "$(basename $0) "[gam-file]" "[.compare-file]" "[output-dir]"
    echo "example: "$(basename $0) '../inputs/sample-0_default' '../inputs/vg-0.compare' '../inputs'
    exit
fi

file=$1
input=$1.gam
output=$3
compare_file=$2
now=$(date '+%d%m%Y%H%M%S')

echo output will be $output/train_file_$now
echo converting gam to json
vg view -a $input > $output/temp_json_$now.json

echo writing file $output/temp_test_$now
python3 jsonParser.py < $output/temp_json_$now.json >$output/temp_test_$now
echo removing $file.json
rm $file.json

echo writing file $output/train_file_$now
python3 makeTestData.py --compare_file $compare_file --tab_converted_file $output/temp_test_$now >$output/train_file_$now
echo removing $output/temp_test_$now
rm $output/temp_test_$now
echo process finished
