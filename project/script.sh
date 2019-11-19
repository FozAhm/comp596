#!/bin/bash
echo Decompression Script
for pathname in /Users/fozail/SchoolDev/comp596/project/data/*.gz; do
    filepath="/Users/fozail/SchoolDev/comp596/project/uncompressed_data/$( basename "$pathname" .gz )"
    gzip -qdc "$pathname" >"$filepath"
    s3path="s3://comp-596-decompressed/$( basename "$pathname" .gz )"
    aws s3 cp $filepath $s3path
    rm $filepath
done
