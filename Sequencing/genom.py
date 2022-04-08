from typing import Dict


def insert(data:Dict, cnx,cur):
    stmt = f"INSERT INTO Research.genoms(id, sequence, organism_type, organism, spezies, subspezies) " \
           f"VALUES(%s,%s,%s,%s,%s, %s);"
    try:
        cur.execute(stmt, data)
        cnx.commit()
        cnx.reconnect()
    except:
        pass