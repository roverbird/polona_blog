#!/bin/bash

md_files="/home/runko/polona/content/*.md"

for file in $md_files; do
  # Remove lines containing '!!int' or '!!null' or "'Tags': []"
  sed -i -e 's/\/[^ ]* \/ [^ ]*\//-/g' -e 's/\/[^ ]*\/[^ ]*\//-/g' $file
done

