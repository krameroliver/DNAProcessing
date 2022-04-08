import os
import warnings
from datetime import date

from Bio import SeqIO
from mysql.connector import MySQLConnection

from Sequencing import Transcription, Translation
from utils.dbConnecion import buildConnection

warnings.simplefilter(action='ignore', category=FutureWarning)
import fnmatch

OPath = r"E:\Data\Virus\INFLUENZA\updates"


# ID, Sequence, organism, sequencing_date, variant, host_organism,organism_type,organism_sub_type, species


def get_updates(opath: str):
    matches = []
    for root, dirnames, filenames in os.walk(opath):
        for filename in fnmatch.filter(filenames, '*.fna'):
            matches.append(os.path.join(root, filename))
    return matches


def insert(to_insert: int):
    data = []
    cnx, cur = buildConnection(db="server")
    cur = cnx.cursor(buffered=True)
    cur.execute('SET GLOBAL max_allowed_packet=6710886400')

    update_versions = get_updates(OPath)
    print(update_versions)
    for variant_path in update_versions:
        variant = ""
        organism = variant_path.split('\\')[3]
        species = "Virus"
        fasta = SeqIO.parse(open(variant_path, 'r'), "fasta")
        print(f"{species}:{variant}")
        for k, record in enumerate(fasta):
            Transcription.procedEntry({
                "id": f'{record.id}',
                "sequence": f'{record.seq}',
                "organism": f'{organism}',
                "sequencing_date": f'{date.today()}',
                "variant": f'{variant}',
                "host_organism": f'HUMAN',
                "organism_type": "",
                "organism_sub_type": "",
                "species": f'{species}'
            })
            Translation.procedEntry({
                "id": f'{record.id}',
                "sequence": f'{record.seq}',
                "organism": f'{organism}',
                "sequencing_date": f'{date.today()}',
                "variant": f'{variant}',
                "host_organism": f'HUMAN',
                "organism_type": "",
                "organism_sub_type": "",
                "species": f'{species}'
            })
            data.append((
                f'{record.id}',
                f'{record.seq}',
                f'{organism}',
                f'{date.today()}',
                f'{variant}',
                f'HUMAN',
                f'',
                f'',
                f'species'
            ))
            if k % to_insert == 0:
                insert_many(data=data, cur=cur,cnx=cnx)
                print(f"{k} rows insertet!")
                data = []
                cnx.commit()
                cnx.reconnect()


def insert_many(data, cnx,cur):
    stmt = f"INSERT INTO Research.genoms(ID, Sequence, organism, sequencing_date, variant, host_organism," \
           f" organism_type,organism_sub_type, species) VALUES(%s,%s,%s,%s,%s, %s, %s, %s,%s);"
    try:
        cur.executemany(stmt, data)
        cnx.commit()
        cnx.reconnect()
    except:
        pass
