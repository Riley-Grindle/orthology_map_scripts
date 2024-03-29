#!/usr/bin/env python3

#####################
## FASTA FORMATTER ##
#####################

import sys
import os



def format_fasta(file, new_fasta, gtf):

    for line in file.readlines():

        if line[0] == ">":

            tilda_1 = line.find("~")
            space = line.find(" ")
            tx_id = line[tilda_1+2:space]

            new_header = gtf[tx_id]

            new_fasta.write(new_header)
            
        else:

            new_fasta.write(line)

def gtf_2_json(gtf, basename):
    

    gtf_dict = {}
    for line in gtf.readlines():
    
        fields = line.split("\t")
        col_9 = fields[8].split(";")

        col_9_dict = {}
        for info in col_9:
            col_9_dict[info.strip().split(" ")[0]] = info.strip().split(" ")[1]

        if fields[2] == 'transcript' or fields[2] == 'RNA' or fields[2] == 'mRNA':
            id = col_9_dict["transcript_id"]
            taxa = basename
            if 'gene_name' in col_9_dict.keys():
                gene = col_9_dict['gene_name']
            elif 'transcript_name' in col_9_dict.keys():
                gene = col_9_dict['transcript_name']
            else:
                gene = id
            
            new_header = ">" + id + "___OX=" + taxa + "___GN=" + gene

            gtf_dict[id] = new_header

    return gtf_dict


            
def main():

    if sys.argv[1] == "-h" or sys.argv[1] == "--h" or sys.argv[1] == "-help" or sys.argv[1] == "--help" :

        print("""\nFASTA FORMATTER:
            
                Use: Format Uniprot fasta files into format of:
                    SEQUENCE-ID__TAX-ID__GENE-SYMBOL
            
                COMMAND: python3 fasta_header_format.py </path/to/input/.fasta> </path/to/output/.fasta>
            
            """)
        exit()

    file_path = sys.argv[1]
    gtf_path = sys.argv[2]
    new_file_path = sys.argv[3]

    fasta = open(file_path, "r")
    new_fasta = open(new_file_path, "w")
    gtf = open(gtf_path, "r")

    basename = os.path.basename(gtf_path)
    gtf_dict = gtf_2_json(gtf, basename)

    format_fasta(fasta, new_fasta, gtf_dict)


if __name__ == "__main__":

    main()



















