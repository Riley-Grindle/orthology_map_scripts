#!/usr/local/bin bash
 

cut -d, -f 4 $1| sed 's/"//g' | while IFS= read line; do
    if [ "$line" != "NA" ]; then
        grep "$line" $2| head -n 1| cut -f 1 >> taxa.tsv
    else
        echo "NA" >> taxa.tsv
     fi
done
