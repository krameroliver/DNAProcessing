import logging
from math import ceil

import pandas as pd
from Bio.Seq import Seq
from Bio.SeqUtils import GC
from joblib import Parallel, delayed
from multiprocessing import cpu_count

from utils.dbConnecion import buildConnection, sqlaConnection, insert_in_table


def getEntrys(limit, offset):
    QUERY = f"select ID from Research.genoms LIMIT {limit},{offset};"
    print(QUERY)
    cnx, cur = buildConnection()
    logging.info("Execute Select")
    print("Execute Select")
    cur.execute(QUERY)
    logging.info("fetch data")
    print("fetch data")
    rows = [i[0] for i in cur.fetchall()]
    cnx.close()
    return rows


def procedEntry(id):
    query = f"select ID, Sequence,organism,sequencing_date from Research.genoms where ID '{id}');"
    data = pd.read_sql_query(sql=query,con=sqlaConnection())
    data['GC_Content'] = data['Sequence'].apply(lambda x : GC(Seq(x)))
    data['AT_Content'] = data['Sequence'].apply(lambda x:  100 - GC(Seq(x)))
    data = data[['ID','GC_Content','AT_Content','organism','sequencing_date']]
    data.to_sql(name="genom_info",if_exists='append',schema='Research',con=sqlaConnection(),index=False)




def main():
    LIMIT = 1000
    ncpu = cpu_count()-1
    cnx, cur = buildConnection()
    cur.execute("TRUNCATE TABLE Research.genom_info;")
    cur.execute(f"select count(ID) from Research.genoms;")
    all = cur.fetchall()[0][0]
    runs = ceil(all / LIMIT)
    for run in range(runs):
        ids = getEntrys(LIMIT, run * LIMIT)
        Parallel(n_jobs=ncpu)(delayed(procedEntry)(i) for i in range(ids))



if __name__ == '__main__':
    main()