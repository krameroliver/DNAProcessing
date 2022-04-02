from typing import Dict

import sqlalchemy
from mysql.connector import MySQLConnection
from sqlalchemy import *
from sqlalchemy import insert


def buildConnection():
    cnx = MySQLConnection(user='Oliver', database='Research', password='KhBHg80C1987.',
                          host='clusterkramer.ddns.net',
                          autocommit=True)
    cur = cnx.cursor(buffered=True)
    cur.execute('SET GLOBAL max_allowed_packet=6710886400')
    return ((cnx, cur))


def sqlaConnection():
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Oliver:KhBHg80C1987.@clusterkramer.ddns.net:3306/Research'
    engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    return engine


def insert_in_table(tablename: str, values: Dict):
    con = sqlaConnection()
    metadata_obj = MetaData(bind=con)
    metadata_obj.reflect(bind=con)
    table = Table(tablename, metadata_obj, autoload=True)
    #table = metadata_obj[tablename]
    #print(table)
    inserts = insert(table).values(values)
    try:
        con.execute(inserts)
    except:
        pass