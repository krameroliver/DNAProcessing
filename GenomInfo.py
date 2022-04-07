import logging

from Bio.Seq import Seq
from Bio.SeqUtils import GC

from utils.dbConnecion import buildConnection


def getEntrys():
    QUERY = f"select ID from Research.genoms;"
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
    query = f"select ID, Sequence,organism,sequencing_date from Research.genoms where ID = '{id}';"
    cnx, cur = buildConnection()
    cur.execute(query)
    data = cur.fetchall()[0]
    gcc = GC(Seq(data[1]))
    atc = 100 - gcc
    sql = f"INSERT INTO Research.genom_info(ID, GC_Content, AT_Content, sequencing_date, organism)VALUES('{id}', {gcc}, {atc}, '{data[3]}', '{data[2]}');commit;"

    try:
        cur.execute(sql)
    except:
        pass



def main():
    cnx, cur = buildConnection()
    cur.execute("TRUNCATE TABLE Research.genom_info;")
    cur.execute(f"select count(ID) from Research.genoms;")
    all = cur.fetchall()[0][0]
    ids = getEntrys()
    for i in ids:
        procedEntry(i)



if __name__ == '__main__':
    main()