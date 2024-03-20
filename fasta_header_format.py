#!/usr/bin/env python3

#####################
## FASTA FORMATTER ##
#####################

import sys

if sys.argv[1] == "-h" or sys.argv[1] == "--h" or sys.argv[1] == "-help" or sys.argv[1] == "--help":

    print("""\nFASTA FORMATTER:
        
            Use: Format Uniprot fasta files into format of:
                 SEQUENCE-ID__TAX-ID__GENE-SYMBOL
          
            COMMAND: python3 fasta_header_format.py </path/to/input/.fasta> </path/to/output/.fasta>
          
          """)
    exit()

file_path = sys.argv[1]
new_file_path = sys.argv[2]

fasta = open(file_path, "r")
new_fasta = open(new_file_path, "w")

def format_fasta(file):

    for line in file.readlines():

        if line[0] == ">":

            index = line.find(">")
            segment = line[index:]
            space = segment.find(" ")
            id = segment[:space]

            index_1 = line.find("OX")
            end_seg_1 = line[index_1:]
            space_1 = end_seg_1.find(" ")
            tax = end_seg_1[:space_1]

            index_2 = line.find("GN")
            end_seg_2 = line[index_2:]
            space_2 = end_seg_2.find(" ")
            gene = end_seg_2[:space_2]

            new_header = id + "__" + tax + "__" + gene + "\n"

            new_fasta.write(new_header)
            
        else:

            new_fasta.write(line)

            



format_fasta(fasta)


















