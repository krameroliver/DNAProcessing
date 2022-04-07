import logging

import numpy as np
from Bio.Seq import Seq

from utils.dbConnecion import buildConnection


def createTable():
    query = f"select ID from Research.genoms where organism = 'SARS' and variant = 'Alpha';"
    cnx, cur = buildConnection()
    logging.info("Execute Select")
    print("Execute Select")
    cur.execute(query)
    header = [i[0] for i in cur.fetchall()]
    print(header)


def getEntrys():
    query = f"select sequence, ID from Research.genoms where organism = 'SARS' and sequence NOT LIKE '%N%' LIMIT 1000;"
    cnx, cur = buildConnection()
    logging.info("Execute Select")
    print("Execute Select")
    cur.execute(query)
    logging.info("fetch data")
    print("fetch data")
    rows = {Seq(i[0]): i[1] for i in cur.fetchall()}
    cnx.close()
    return rows

def defineMatrix():
    query = f"select count(ID) from Research.genoms where organism = 'SARS'and variant = 'Alpha' ;"
    cnx, cur = buildConnection()
    logging.info("Execute Select")
    print("Execute Select")
    cur.execute(query)
    sizeing = cur.fetchall()[0][0]
    Martrix = np.zeros((sizeing,sizeing))
    return Martrix

if __name__ == '__main__':
    #liste = createTable()
    defineMatrix()