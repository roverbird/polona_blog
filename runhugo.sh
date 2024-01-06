#!/bin/bash

# Set the number of files you want to process
N=10

# Get the first N Markdown files
md_files=$(ls /home/runko/polona/content/ | head -n $N)

# Run Hugo with the selected files
hugo -s /home/runko/polona -d /var/www/sotoff/polona "$md_files"

