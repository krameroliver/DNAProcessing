import pandas as pd
from utils.dbConnecion import sqlaConnection


def readProp(path):
    data = pd.read_csv(path,header=0,delimiter=";")
    #data.set_index(keys="Variante",inplace=True)
    data.to_sql(schema="Research",if_exists="replace",con=sqlaConnection(),name="CovidPropertys",index=False)


readProp("resources/propertys.tsv")
