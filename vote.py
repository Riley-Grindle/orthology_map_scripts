#!/Users/rgrindle/miniforge3/bin/python3


import sys
import json

def extract_gene_id(query_list):

    gene_dict = {}
    for line in query_list:
        gene_dict[(line[1:line.index("~")])] = dict()
    
    return gene_dict

def combine(agg, comp):

    for key, value in comp.items():
        if key == "tool":
            continue
        if key in list(agg.keys()):
            common_genes = set(value.keys()).intersection(set(agg[key].keys()))
            if len(common_genes) > 0:
                for gene in common_genes:
                   agg[key][gene] = agg[key][gene] + comp[key][gene]
            else:
                for gene in list(value.keys()):
                    agg[key][gene] = comp[key][gene]

    return agg

def tuplify(comp, tool):

    for key, value in comp.items():
        if key == "tool":
            continue
        for gene, info in value.items():
            comp[key][gene] = [tuple([taxa, tool]) for taxa in info]
    
    return comp

def main():

    with open(sys.argv[1], "r") as query_file:
        query_list = query_file.readlines()

    q_genes = extract_gene_id(query_list)
    
    with open(sys.argv[3], "r") as comparing_file:
        comparison = json.load(comparing_file)

    with open(sys.argv[2], "r") as aggregate_file:
        try:
            aggregate  = json.load(aggregate_file)
            
        except json.decoder.JSONDecodeError :
            
            aggregate = q_genes
    aggregate_file.close()

    formatted_comp = tuplify(comparison, comparison["tool"])
    new_aggregate  = combine(aggregate, formatted_comp)

    with open(sys.argv[2], "w") as outfile:
        json.dump(new_aggregate, outfile, indent=4)
    outfile.close()
    

if __name__ == "__main__":
    main()
