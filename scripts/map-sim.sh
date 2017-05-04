#!/bin/bash

if [ $# -ne 3 ];
then
    echo "usage: "$(basename $0) "[input-file] [output-file] [vg-dir]"
    echo "example: "$(basename $0) "../output/output_1M ../output/ /usr/home/vg/"
    exit
fi
now=$(date '+%d%m%Y%H%M%S')
input=$1
output=$2
vg_dir=$3
#mkdir -p $output

echo combining results
( cat $input | awk 'BEGIN { OFS="\t"; print "correct", "mq", "score", "aligner"; } { print $5, $4, $3, "vg-lr" }' ;
  cat $input | awk 'BEGIN { OFS="\t"} { print $5, $2, $3, "vg" }' ;) | gzip >$output/results-vg_$now.tsv.gz

# This can then be rendered using scripts in the vg repo
echo rendering ROC
rscript $vg_dir/scripts/plot-roc.R $output/results-vg_$now.tsv.gz $output/roc-vg-vglr_$now.pdf
echo rendering QQ
rscript $vg_dir/scripts/plot-qq.R $output/results-vg_$now.tsv.gz $output/qq-vg-vglr_$now.pdf
