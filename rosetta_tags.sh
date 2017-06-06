#!/usr/bin/env bash
# "ant -Dbt.arch=amd64-glibc212-gcc44 MultiLangRLP -Dmultilang.input=1 -DoutputFile=out1.txt"

FILES="/home/shadowtrader/PycharmProjects/ner/test_docs/*"
OUTPUT_DIR="/home/shadowtrader/PycharmProjects/ner/rosetta_tags/"

for f in $FILES
do
  echo "Processing $f file..."
  ant -Dbt.arch=amd64-glibc212-gcc44 MultiLangRLP -Dmultilang.input="$f" -DoutputFile="$f".txt
done