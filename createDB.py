import sqlite3
import pandas as pd


def createDataTable():
    con = sqlite3.connect("SI.db")
    df = pd.read_csv("netflix_titles.csv",sep = ';', header=0)
    df.to_sql("show", con, schema = None, if_exists= 'replace', index = False)
    con.commit()

def num_samples():
    con = sqlite3.connect("SI.db")
    frase = "SELECT COUNT(*) FROM show WHERE show_id IS NOT NULL AND type IS NOT NULL AND title IS NOT NULL AND " \
            "director IS NOT NULL AND country NOT NULL AND date_added NOT NULL AND " \
            "release_year NOT NULL AND rating NOT NULL AND duration NOT NULL AND listed_in NOT NULL AND " \
            "description NOT NULL AND cast NULL"
    tam = pd.read_sql_query(frase,con)
    print("Numero de muestras sin missing values: " + str(tam))

createDataTable()
num_samples()
