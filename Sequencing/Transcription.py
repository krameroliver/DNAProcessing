import logging

import pandas as pd
from Bio.Seq import Seq

from utils.dbConnecion import buildConnection, sqlaConnection


def getEntrys():
    QUERY = f"select ID from Research.genoms;"
    cnx, cur = buildConnection()
    logging.info("Execute Select")
    print("Execute Select")
    cur.execute(QUERY)
    logging.info("fetch data")
    print("fetch data")
    rows = [i[0] for i in cur.fetchall()]
    cnx.close()
    return rows


def procedEntry(info):
    print("Proceed RNA")
    sequence = info['sequence']
    tr = sequence.transcribe()
    id = info['id']
    organism = info['organism']
    sequencing_date = info['sequencing_date']
    variant = info['variant']
    rnaSeq = sequence.transcribe().upper()
    d = [[id,organism,f"{sequencing_date}",variant,f"{rnaSeq}"]]
    data = pd.DataFrame(d,columns=['id','organism','seq_date','variant','ssmRNA'])
    try:
        data.to_sql(index=False, if_exists='append', schema='Research', con=sqlaConnection(db='server'), name='ssmRNA')
    except:
        pass


