#!/usr/bin/bash

mkdir "./tree_info"

grep -o "^.*.PTHR.*.SF[^;]*" *.out > cleaned.txt

grep -Eo "NAME:[^;]+" *.out | cut -c 6- > prot_names.txt

sed 's/\(PTHR.*\)//' cleaned.txt > sequence_headers.txt

touch "orthologs.txt"

while read p; do
  echo $p | grep -o "SF.*" | cut -c 4-
done < cleaned.txt > subfamilies.txt

while read p; do
  echo $p | grep -o "PTHR.*:" | rev | cut -c2- | rev
done < subfamilies.txt > families.txt

count=1

while IFS= read -r F; do
    output_file="./tree_info/tree$count.json"
    curl -X GET "https://www.pantherdb.org/services/oai/pantherdb/treeinfo?family=$F" -H "accept: application/json" > "$output_file"
    count=$((count+1))
done < families.txt

mkdir "./genes"

count=1
find "./tree_info" -maxdepth 1 -type f -exec stat -f "%B %N" {} + | sort -n | while read -r creation_time file_path; do

    SF=$(sed -n "${count}p" subfamilies.txt)

    grep -A 100 "$SF" "$file_path" | grep "gene_id" | tr -d '[:space:]' > "genes/genes$count.txt"

    count=$((count+1))
done

count=1
for file in "./genes"/*; do 

    
    if [ -s $file ]; then

        echo "File is not empty"

    else

        echo -e "File is empty...\nNo subfamily matches in Panther db\nSearching by protein name...."
        file_1=$(ls -1 "./tree_info" | awk "NR==$count")
        index=$(echo $file_1 | grep -oE '[0-9]+')
        name=$(sed -n "${index}p" prot_names.txt)
        grep -A 100 "$name" "./tree_info/$file_1" | grep "gene_id" | tr -d '[:space:]' > genes/genes$index.txt


    fi
    count=$((count+1))
done


count=1
while IFS= read -r id; do

    gene_file="./genes/genes$count.txt"

    echo "$id" >> "orthologs.txt"
    echo -e "_________________________\n" >> "orthologs.txt"
    cat "$gene_file" >> "orthologs.txt"

    echo -e "\n_______________________________________________________________________\n" >> "orthologs.txt"

    count=$((count+1))

done < sequence_headers.txt
