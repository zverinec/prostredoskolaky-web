#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: ./unzip-web-data.sh file.zip"
    exit 1
fi

rm -r 'static/drive-data'
yes | unzip $1 'web-data/*' -d 'static/drive-data'
mv static/drive-data/web-data/* 'static/drive-data'
rmdir 'static/drive-data/web-data'

echo ""
echo "Some largest static files (check for size):"
ls -lhS 'static/drive-data' | head
