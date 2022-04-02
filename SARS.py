import os
import warnings
from datetime import date

import pandas as pd
import sqlalchemy
from Bio import SeqIO
from mysql.connector import MySQLConnection

import utils.parsePropertys as pp

warnings.simplefilter(action='ignore', category=FutureWarning)
import fnmatch


def get_type(opath: str):
    matches = []
    for root, dirnames, filenames in os.walk(opath):
        for filename in fnmatch.filter(filenames, '*.fna'):
            matches.append(os.path.join(root, filename))
    return matches


def get_type_infos(path: str):
    subs = path.split("\\")
    infos = {'species': subs[2], 'organism': subs[3], 'organism_type': subs[4], 'variant': subs[5],
             "organism_sub_type": subs[5]}
    return infos


def organismtype(otype: str = "Virus"):
    root = pp.getFileSource()
    opath = os.path.join(root, otype)

    organismtypes = []

    for i in get_type(opath=opath):
        organismtypes.append((i, get_type_infos(i)))
    return organismtypes


def insert(to_insert: int):
    data = []

    cnx = MySQLConnection(user='Oliver', database='Research', password='KhBHg80C1987.',
                          host='clusterkramer.ddns.net',
                          autocommit=True)
    cur = cnx.cursor(buffered=True)
    cur.execute('SET GLOBAL max_allowed_packet=6710886400')

    for f in organismtype():
        FPATH = f[0]
        infos = f[1]
        fasta = SeqIO.parse(open(FPATH, 'r'), "fasta")
        print(f"{infos['organism']}:{infos['species']}:{infos['variant']}")

        for k, record in enumerate(fasta):
            data.append((
                f'{record.id}',
                f'{record.seq}',
                f'{infos["organism"]}',
                f'{date.today()}',
                f'{infos["variant"]}',
                f'HUMAN',
                f'{infos["organism_type"]}',
                f'{infos["organism_sub_type"]}',
                f'{infos["species"]}'
            ))
            if k % to_insert == 0:
                insert_many(data=data, cur=cur)
                print(f"{k} rows insertet!")
                data = []
                cnx.commit()
                cnx.reconnect()


def insert_many(data, cur):
    stmt = f"INSERT INTO Research.genoms(ID, Sequence, organism, sequencing_date, variant, host_organism," \
           f" organism_type,organism_sub_type, species) VALUES(%s,%s,%s,%s,%s, %s, %s, %s,%s);"
    cur.executemany(stmt, data)


def count_table(TABLE, variant: str, org_type: str):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Oliver:KhBHg80C1987.@clusterkramer.ddns.net:3306/Research'
    engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    sql = f"select count(*) as c from Research.{TABLE} where variant='{variant}' and organism_type='{org_type}';"
    counter = pd.read_sql(sql=sql, con=engine)
    print("Entrys: " + str(counter.loc[0, 'c']))
    return counter.loc[0, 'c']
