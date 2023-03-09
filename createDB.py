import math
import sqlite3

import numpy as np
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
            "description NOT NULL and 'cast' NOT NULL"
    tam = pd.read_sql_query(frase,con).values[0][0]
    print("Numero de muestras completas (sin missing values): " + str(tam))

def med_duracion():
    con = sqlite3.connect("SI.db")
    frase = "SELECT AVG(duration) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    frase2 = "SELECT AVG(duration) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    med_film = pd.read_sql_query(frase, con).values[0][0]
    med_show = pd.read_sql_query(frase2, con).values[0][0]
    print("Duración media (películas): " + str(round(med_film))+ " minutos")
    print("Duración media (series): " + str(round(med_show)) + " temporadas")

def des_duracion():
    con = sqlite3.connect("SI.db")
    frase = "SELECT AVG(duration * duration) - AVG(duration) * AVG(duration) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    frase2 = "SELECT AVG(duration * duration) - AVG(duration) * AVG(duration) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(frase, con).values[0][0] ** 0.5
    std_show = pd.read_sql_query(frase2, con).values[0][0] ** 0.5
    print("Desviación típica de la duración (películas): " + str(round(std_film, 2)))
    print("Desviación típica de la duración (series): " + str(round(std_show, 2)))

createDataTable()
num_samples()
med_duracion()
des_duracion()

