#!/usr/bin/env sh
echo "Sample app running"
date
echo "Creating marker file"
mkdir -p /data/local/tmp/rdcr_sample
echo "ran at $(date)" > /data/local/tmp/rdcr_sample/marker.txt
echo "Done"
