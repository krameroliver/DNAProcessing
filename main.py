import os
import threading

from Bio import SeqIO

from Sequencing.Transcription import insert as trainsert
from Sequencing.Translation import insert as tralinsert
from Sequencing.genom import insert as ginsert
from parsePropertys import getFileSource
from utils.buildGenomConfig import getGenomConfig, findPossibleFiles
from utils.dbConnecion import buildConnection


def main():
    src = getFileSource()
    orga = getGenomConfig()
    organism_type = list(orga.keys())[0]
    organisms = list(orga[organism_type].keys())
    print(organisms)
    pathes = findPossibleFiles(os.path.join(src, organism_type))

    pathes = [i for i in pathes if organisms[0] in i or organisms[1] in i]
    for p in pathes:
        run(p)


def run(path: str):
    cnx, cur = buildConnection(db="server")
    cur.execute('SET GLOBAL max_allowed_packet=6710886400')
    fasta = SeqIO.parse(open(path, 'r'), "fasta")
    infos = path.split(os.sep)[2:]
    for k, record in enumerate(fasta):
        data = {"id": record.id,
                "sequence": record.seq,
                "organism_type": infos[0],
                "organism": infos[1],
                "spezies": infos[2],
                "subspezies": infos[3]
                }

        genomm = threading.Thread(target=ginsert, args=(data,cnx,cur))
        rna = threading.Thread(target=ginsert, args=(trainsert, cnx, cur))
        protein = threading.Thread(target=ginsert, args=(tralinsert, cnx, cur))
        genomm.start()
        rna.start()
        protein.start()
        genomm.join()
        rna.join()
        protein.join()
        cnx.commit()
        cnx.reconnect()
    cnx.close()


if __name__ == '__main__':
    main()
