#!/usr/bin/env bash

FILES="/home/shadowtrader/PycharmProjects/ner/10_docs/*"
OUTPUT_DIR="/home/shadowtrader/PycharmProjects/ner/10_tags/"

for f in $FILES
do
  echo "Processing $f file..."
  /home/shadowtrader/repos/protext-lib/categorization/SequenceClassification/test_sequence_classification -NER < "$f" > "$f".txt
done