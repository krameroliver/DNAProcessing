import logging

import pandas as pd
from Bio.Seq import Seq

from utils.dbConnecion import buildConnection, sqlaConnection

def procedEntry(info):
    print("Proceed RNA")
    sequence = info['sequence']
    tr = sequence.transcribe()
    id = info['id']
    organism = info['organism']
    sequencing_date = info['sequencing_date']
    variant = info['variant']
    prot = sequence.translation().upper()
    d = [[id, organism, f"{sequencing_date}", variant, f"{prot}"]]
    data = pd.DataFrame(d, columns=['id', 'organism', 'seq_date', 'variant', 'ssmRNA'])
    try:
        data.to_sql(index=False, if_exists='append', schema='Research', con=sqlaConnection(db='server'), name='protein')
    except:
        pass


