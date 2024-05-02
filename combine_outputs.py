#!/opt/homebrew/bin/python3


import json
import sys


def main():

    with open(sys.argv[2], "r") as comp:
        comparison = json.load(comp)

    with open(sys.argv[1], "r") as agg:
        try:
            aggregate  = json.load(agg)

        except json.decoder.JSONDecodeError :
            agg.close()
            with open(sys.argv[1], "w") as output:
                json.dump(comparison, output, indent=4)
            output.close()
            exit()

    for gene, matches in comparison.items():
        
        if not gene in list(aggregate.keys()):
            aggregate[gene] = matches

        else:

            for match, species in matches.items():

                if not match in list(aggregate[gene].keys()):
                    aggregate[gene][match] = species
                
                else:
                    aggregate[gene][match] = set(aggregate[gene][match])
                    aggregate[gene][match] = aggregate[gene][match].union(set(species))
                    aggregate[gene][match] = list(aggregate[gene][match])

    agg.close()       
    with open(sys.argv[1], "w") as output:
        json.dump(aggregate, output, indent=4)
    output.close()
    

if __name__ == "__main__":

    main()