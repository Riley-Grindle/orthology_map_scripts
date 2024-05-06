#!/usr/local/bin/python3

import sys
import json



def main():

    with open(sys.argv[1], "r") as aggregate_file:
        aggregate = json.load(aggregate_file)
    aggregate_file.close()

    for query, genes in aggregate.items():
        for gene, species_tool in genes.items():
            aggregate[query][gene] = dict()
            for tup in species_tool:
                if tup[0] in list(aggregate[query][gene].keys()):
                    aggregate[query][gene][tup[0]] = set(aggregate[query][gene][tup[0]])
                    aggregate[query][gene][tup[0]].add(tup[1])
                    aggregate[query][gene][tup[0]] = list(aggregate[query][gene][tup[0]])
                else:
                    aggregate[query][gene][tup[0]] = [tup[1]]
    
    with open(sys.argv[1], "w") as outfile:
        json.dump(aggregate, outfile, indent=4)
    outfile.close()
    

if __name__ == "__main__":
    main()