#!/usr/bin/env python3

import sys
import csv
import json
import os

# Trailing Arg 1 = tree_std.csv file
# Trailing Arg 2 = prefix_2_file.json
# Trailing Arg 3 = Path_to_dataset_jsons


def get_prefix(ensembl_id):
    """"""

    # Human prefix
    try :
        tmp = int(ensembl_id[3])
        prefix = ensembl_id[:3]
    except ValueError:
        pass

    # Edge case prefix's
    if ensembl_id[:14] == "MGP_PahariEiJ_":
        prefix == "MGP_PahariEiJ_"
    elif ensembl_id[:7] == "ENSHGLF":
        prefix = "ENSHGLF"
    elif ensembl_id[:14] == "MGP_CAROLIEiJ_":
        prefix = "MGP_CAROLIEiJ_"
    elif ensembl_id[:13] == "MGP_SPRETEiJ_":
        prefix = "MGP_SPRETEiJ_"
    elif ensembl_id[:7] == "ENSCSAV":
        prefix = "ENSCSAV"

    # Normal 6 digit prefix
    else:
        prefix = ensembl_id[:6]



    return prefix




def get_data_file(prefix, prefix_2_json_file):
    """"""

    data_file = prefix_2_json_file[prefix]

    return data_file


def get_gene_symbol(ensembl_id, json_file, data_dir):
    """"""

    if data_dir[-1] == "/":
        path_to_file = data_dir + json_file
    else:
        path_to_file = data_dir + "/" + json_file

    json_file = open(path_to_file, "r")
    gene_info_dict = json.load(json_file)

    if ensembl_id[-2] == ".":
        try:
            gene_symbol = gene_info_dict[ensembl_id[:-2]]
        except KeyError:
            gene_symbol = "NA"
    else:
        try:
            gene_symbol = gene_info_dict[ensembl_id]
        except KeyError:
            gene_symbol = "NA"

    return gene_symbol


def main():

    ###############################################
    # Load in Working data and supplementary files.
    ###############################################
    try:
        gene_id_file = open(sys.argv[1], "r")
        gene_id_csv = csv.reader(gene_id_file, delimiter= ",")

    except FileNotFoundError and IndexError:
        print("\nThe input file does not exist or was not provided.\n")


    try:
        prefix_2_json = open(sys.argv[2], "r")
        prefix_dict = json.load(prefix_2_json)

    except FileNotFoundError and IndexError:
        print("\nThe input json file does not exist or was not provided.\n")

    try:
        json_data_dir = sys.argv[3]

        if os.path.isdir(json_data_dir):
            pass
        else:
            raise Exception("\nJson data directory does not exist.\n")

    except IndexError:
        print("\nNo input provided for path to json data.\n")

    try:
        prefix_2_species = open(sys.argv[4], "r")
        species = json.load(prefix_2_species)

    except FileNotFoundError and IndexError:
        print("\nThe input species json file does not exist or was not provided.\n")
    ################################################
    ################################################
    ################################################


    # Format ortholog data into a list
    gene_id_list = []
    for line in gene_id_csv:
        gene_id_list.append(line[1])


    # main control structure
    gene_symbol_str = "\"GENE\"\n"
    species_str = "\"SPECIES\"\n"
    counter = 0
    for id in gene_id_list:

        if id == "MATCH":
            continue

        if id[0:8] == "Ensembl:":

            prefix          = get_prefix(id[8:])
            species_str     = species_str + "\"" + species[prefix].strip() + "\"\n"
            data_file       = get_data_file(prefix, prefix_dict)
            gene_symbol     = get_gene_symbol(id[8:], data_file, json_data_dir)
            gene_symbol_str = gene_symbol_str + "\"" + gene_symbol + "\"\n"

        else:
            gene_symbol_str = gene_symbol_str + "\"" + "NA" + "\"\n"
            species_str     = species_str + "\"" + "NA" + "\"\n"


    with open("gene_symbols_ensembl.txt", "w") as gene_symbols_file:
        gene_symbols_file.write(gene_symbol_str)

    with open("species_names.txt", "w") as species_file:
        species_file.write(species_str)



if __name__ == "__main__":

    main()


