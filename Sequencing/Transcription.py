from typing import Dict

from Bio.Seq import Seq


def insert(data: Dict, cnx, cur):
    data_neu = {"id": data["id"],
                "sequence": Seq(data["sequence"]).transcribe().upper(),
                "organism_type": data["organism_type"],
                "organism": data["organism"],
                "spezies": data["spezies"],
                "subspezies": data["subspezies"]}
    stmt = f"INSERT INTO Research.ssmRNA(id, sequence, organism_type, organism, spezies, subspezies) " \
           f"VALUES(%s,%s,%s,%s,%s, %s);"
    try:
        cur.execute(stmt, data_neu)
        cnx.commit()
        cnx.reconnect()
    except:
        pass
