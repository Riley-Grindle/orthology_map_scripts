#!/usr/bin/env python3

# Python3 code to implement iterative Binary
# Search.

import sys
import json


# Driver Code
if __name__ == '__main__':
    name = sys.argv[1]
    file = open(name, "r")
    dict_ids = json.load(file)

    
    target_name = sys.argv[2]
    file_target = open(target_name, "r")
    target_list = file_target.readlines()
    
    
    # Dictionary Search
    gene_symbols = list()
    species_list = list()
    for i in range(len(target_list)):

        if i > 0:
            result = dict_ids[target_list[i].strip()]
            gene_symbols.append(result.strip())
            tmp_lst = [*target_list[i]]
            index = tmp_lst.index(".")
            species_list.append(target_list[i][:index])

    long_string = "GENE\n"
    spec_long_string = "SPECIES\n"
    for i in range(len(gene_symbols)):
        long_string = long_string + gene_symbols[i] + "\n"
        spec_long_string = spec_long_string + species_list[i] + "\n"

    with open("gene_symbols.txt", "w") as gene_file:
        gene_file.write(long_string)

    with open("taxa_ids.txt", "w") as species_file:
        species_file.write(spec_long_string)

    gene_file.close()


