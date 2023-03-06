import sqlite3
import pandas as pd


def createDataTable():
    con = sqlite3.connect("SI.db")
    df = pd.read_csv("netflix_titles.csv",sep = ';', header=1)
    df.to_sql("show", con, schema = None, if_exists= 'replace', index = False)
    con.commit()


createDataTable()
