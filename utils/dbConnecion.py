from typing import Dict

import sqlalchemy
import yaml
from mysql.connector import MySQLConnection
from sqlalchemy import *
from sqlalchemy import insert


def buildConnection(db: str):
    assert db in ('nas', 'server'), "Database decision not nas or server"
    with open('genom.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

        cnx = MySQLConnection(user=config[db]['user'], database='Research', password=config[db]['pw'],
                              host=config[db]['host'],
                              autocommit=True)
        cur = cnx.cursor(buffered=True)
        cur.execute('SET GLOBAL max_allowed_packet=6710886400')
        return (cnx, cur)


def sqlaConnection(db: str):
    assert db in ('nas', 'server'), "Database decision not nas or server"
    with open('genom.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{config[db]["user"]}:{config[db]["pw"]}@{config[db]["host"]}:{config[db]["port"]}/Research'
        engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
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