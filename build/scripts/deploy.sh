#!/bin/bash

echo -e "Content-type: text/html\n"

OUTPUT+=$(git fetch origin 2>&1)$'\n\n'
if [ $? -eq 0 ]; then
	OUTPUT+=$(git reset --hard origin/master 2>&1)$'\n\n'
fi

if [ $? -eq 0 ]; then
	OUTPUT+=$(cd ../.. && make all 2>&1)$'\n\n'
fi

echo "$OUTPUT" | mail -a "Content-Type: text/plain; charset=UTF-8" \
    -s "[prostredoskolaky-web] Deploy status" "prostredoskolaky@fi.muni.cz"
