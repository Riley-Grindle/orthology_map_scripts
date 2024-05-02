#!/usr/bin/python3

import sys
import os


def gtf_2_dict(gtf_file):

    gtf = open(gtf_file, "r")
    gtf_list = gtf.readlines()

    gtf_dict = {}
    for line in gtf_list:
        fields = line.split("\t")
        col_9 = fields[8].split(";")

        column_9_dict = {}
        for i in range(len(col_9)-1):
            key_value = col_9[i].strip().split("\"")
            column_9_dict[key_value[0][:-1]] = key_value[1]

        if fields[2] == 'transcript':
            gtf_dict[column_9_dict['transcript_id']] = [fields[0], fields[3], fields[4]]

        
    return gtf_dict
    


def get_blastp_eval(results, gtfQ, gtfM):

    results_tbl = open(results, "r")
    results_list = results_tbl.readlines()

    new_lines = []
    for match in results_list:
        fields = match.split("\t")
        tilda = fields[0].find("~")
        period = fields[0][::-1].find(".") - (2 * (fields[0][::-1].find("."))) - 1

        txid_query = fields[0][tilda+2:period]  
        txid_match = fields[1][:fields[1].find("_")]
        
        index = [idx for idx, id in enumerate(list(gtfQ.keys())) if txid_query in id][0]
        txid_query = list(gtfQ.keys())[index]
        index = [idx for idx, id in enumerate(list(gtfM.keys())) if txid_match in id][0]
        txid_match = list(gtfM.keys())[index]

        string_Q = make_df(txid_query, gtfQ[txid_query])
        string_M = make_df(txid_match, gtfM[txid_match])

        new_lines.append(string_Q + "\t" + string_M + "\t" + fields[10])

    return new_lines




def make_df(tx_id, list):

    string = list[0] + "\t" + tx_id + "\t" + list[1] + "\t" + list[2]

    return string

def main():

    gtf_Q_file = sys.argv[1]
    gtf_M_file = sys.argv[2]
    blast_res = sys.argv[3]

    dict_Q = gtf_2_dict(gtf_Q_file)
    dict_M = gtf_2_dict(gtf_M_file)

    new_df_lines = get_blastp_eval(blast_res, dict_Q, dict_M)

    new_file = ""
    for line in new_df_lines:
        new_file = new_file + line + "\n"

    with open("dagchainer.db.tsv", "w") as file:
        file.write(new_file)

    file.close()

    


if __name__ == "__main__":

    main()
