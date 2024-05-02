#!/opt/homebrew/bin/python3

import sys
import json


def parse_hits(tbl_lst):

    genes = dict()
    for i in range(1,len(tbl_lst)):
        
        try:
            tbl_lst[i].index("~")

            if (tbl_lst[i].split("~")[0]) in list(genes.keys()):
                pass
            else:
                genes[(tbl_lst[i].split("~")[0])] = list()
            
            key = (tbl_lst[i].split("~")[0])

            if tbl_lst[i].split("\t")[2] != "NA" and tbl_lst[i].split("\t")[2] != "NO GENE SYMBOL":
                genes[key].append((tbl_lst[i].split("\t")[2].upper(), tbl_lst[i].split("\t")[3].strip()))
            
        except ValueError:
            if tbl_lst[i].split("\t")[2] != "NA" and tbl_lst[i].split("\t")[2] != "NO GENE SYMBOL":
                genes[key].append((tbl_lst[i].split("\t")[2].upper(), tbl_lst[i].split("\t")[3].strip()))
        

    return genes

def join_hits(match_list):

    tmp_dict = dict()
    for match in match_list:
        if not (match[0] in list(tmp_dict.keys())):
            tmp_dict[match[0]] = set()
            tmp_dict[match[0]].add(match[1])
            tmp_dict[match[0]] = list(tmp_dict[match[0]])
        else:
            tmp_dict[match[0]] = set(tmp_dict[match[0]])
            tmp_dict[match[0]].add(match[1])
            tmp_dict[match[0]] = list(tmp_dict[match[0]])

    return tmp_dict

def main():

    file = open(sys.argv[1], "r")

    file_lst = file.readlines()

    genes = parse_hits(file_lst)
    for gene, match in genes.items():

        revised_match = join_hits(match)
        genes[gene] = revised_match
    
    
    try:
        file_name = sys.argv[2] + "." + sys.argv[3] + ".query_2_matches.json"
        genes["tool"] = sys.argv[3]

    except IndexError:
        file_name = sys.argv[2] + ".query_2_matches.json"
        genes["tool"] = sys.argv[2]     
   
    with open(file_name, "w") as output:
        json.dump(genes, output, indent=4)

if __name__ == "__main__":
    main()
