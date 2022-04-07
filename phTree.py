from typing import Dict

from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

from utils.dbConnecion import buildConnection


def ofile(indict:Dict):
    list_seq =list(indict.keys())
    list_name = list(indict.values())
    ofile = open("my_fasta.txt", "w")
    for i in range(len(list_seq)):
        if len(list_seq[i]) > 27000:
            ofile.write(">" + list_name[i] + "\n" + list_seq[i][:27000] + "\n")

    # do not forget to close it

    ofile.close()

def getData():
    query = f"select sequence,ID from Research.genoms where organism = 'SARS';"
    cnx, cur = buildConnection()
    print("Execute Select")
    cur.execute(query)
    list_seq = list([i[0] for i in cur.fetchall()])
    list_name = list([i[1] for i in cur.fetchall()])
    ofile = open("my_fasta.txt", "w")
    for i in range(len(list_seq)):
        if len(list_seq[i]) > 27000:
            ofile.write(">" + list_name[i] + "\n" + list_seq[i][:27000] + "\n")

def main():
    getData()

    align = AlignIO.read(open("my_fasta.txt"), "fasta")

    calculator = DistanceCalculator('identity')
    distMatrix = calculator.get_distance(align)


    constructor = DistanceTreeConstructor()# Construct the phlyogenetic tree using UPGMA algorithm
    UGMATree = constructor.upgma(distMatrix)# Construct the phlyogenetic tree using NJ algorithm
    NJTree = constructor.nj(distMatrix)
    # Draw the phlyogenetic tree
    #Phylo.draw(UGMATree)# Draw the phlyogenetic tree using terminal

    tree = Phylo.draw_ascii(NJTree)
    tree.draw()
    tree.savefig('tree.png')

main()