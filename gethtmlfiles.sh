#!/bin/sh
TYPE="oth"
paste data/names_$TYPE.txt data/links_$TYPE.txt | while IFS="$(printf '\t')" read -r name link
do
    wget -O "html/$TYPE/$name" "$link"
    sleep 1
done