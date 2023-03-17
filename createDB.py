import random
import re
import sqlite3
import pandas as pd
import numpy
from matplotlib import pyplot as plt


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

def max_duracion():
    con = sqlite3.connect("SI.db")
    frase = "SELECT MAX(CAST(duration as integer)) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    frase2 = "SELECT MAX(CAST(duration as integer)) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(frase, con).values[0][0]
    std_show = pd.read_sql_query(frase2, con).values[0][0]
    print("Máxima duración de una película: " + str(std_film)+ " minutos")
    print("Máxima duración de una serie: " + str(std_show) + " temporadas")

def min_duracion():
    con = sqlite3.connect("SI.db")
    frase = "SELECT MIN(CAST(duration as integer)) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    frase2 = "SELECT MIN(CAST(duration as integer)) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(frase, con).values[0][0]
    std_show = pd.read_sql_query(frase2, con).values[0][0]
    print("Mínima duración de una película: " + str(std_film)+ " minutos")
    print("Mínima duración de una serie: " + str(std_show) + " temporadas")

def anio():
    con = sqlite3.connect("SI.db")
    frase = "SELECT MAX(CAST(release_year as integer)) FROM show WHERE release_year IS NOT NULL"
    frase2 = "SELECT MIN(CAST(release_year as integer)) FROM show WHERE release_year IS NOT NULL"
    maxanio = pd.read_sql_query(frase, con).values[0][0]
    minanio = pd.read_sql_query(frase2, con).values[0][0]
    print("Año de publicación más reciente: " + str(maxanio) )
    print("Año de publicación más antiguo: " + str(minanio) )

def group_dataframe():
    con = sqlite3.connect("SI.db")
    frase = "SELECT  * FROM show WHERE type = 'Movie' AND CAST(duration as integer) >= 90 "
    frase2 = "SELECT  *  FROM show WHERE type = 'Movie' AND CAST(duration as integer) < 90 "
    frase3 = "SELECT  *  FROM show WHERE type = 'TV Show' AND CAST(duration as integer) > 2 "
    frase4 = "SELECT * FROM show WHERE type = 'TV Show' AND CAST(duration as integer) <= 2 "
    frase5 = "SELECT  *  FROM show WHERE type = 'Movie'"
    frase6 = "SELECT  *  FROM show WHERE type = 'TV Show'"
    f1 = pd.read_sql_query(frase, con)
    f2 = pd.read_sql_query(frase2, con)
    f3 = pd.read_sql_query(frase3, con)
    f4 = pd.read_sql_query(frase4, con)
    f5 = pd.read_sql_query(frase5, con)
    f6 = pd.read_sql_query(frase6, con)
    f1['duration'] = f1['duration'].apply(lambda x: re.sub('[^0-9]','',x)).astype(int)
    f2['duration'] = f2['duration'].apply(lambda x: re.sub('[^0-9]','', x)).astype(int)
    f3['duration'] = f3['duration'].apply(lambda x: re.sub('[^0-9]','', x)).astype(int)
    f4['duration'] = f4['duration'].apply(lambda x: re.sub('[^0-9]','', x)).astype(int)
    return f1,f2,f3,f4,f5,f6

def info_f(f):
    print("Número : "+str(f['duration'].shape[0]))
    print("Mediana: "+ str(f['duration'].median()))
    print("Media: " + str(round(f['duration'].mean(), 2)))
    print("Varianza: " + str(round(f['duration'].var(), 2)))
    print("Máximo: " + str(f['duration'].max()))
    print("Mínimo: " + str(f['duration'].min()))

def info_p(f):
    print("Número : "+str(f['duration'].shape[0]))
    print("Valores nulos: "+str(f['duration'].isnull().sum()))
    f['duration'] = f['duration'].dropna().apply(lambda x: re.sub('[^0-9]', '', x)).astype(int)
    print("Mediana: "+ str(f['duration'].median()))
    print("Media: " + str(round(f['duration'].mean(), 2)))
    print("Varianza: " + str(round(f['duration'].var(), 2)))
    print("Máximo: " + str(f['duration'].max()))
    print("Mínimo: " + str(f['duration'].min()))

def tabla_usuarios():
    con = sqlite3.connect("SI.db")
    df = pd.read_csv("datos.csv", sep=',', header=0)
    df.to_sql("user", con, schema=None, if_exists='replace', index=False)
    con.commit()
def tabla_visionados():
    conexion = sqlite3.connect("SI.db")
    conexion.execute('''CREATE TABLE IF NOT EXISTS visionados
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             id_pelicula INTEGER NOT NULL,
             id_usuario INTEGER NOT NULL,
             puntuacion REAL,
             FOREIGN KEY(id_pelicula) REFERENCES show(show_id),
             FOREIGN KEY(id_usuario) REFERENCES user(id),
             UNIQUE(id_pelicula, id_usuario))''')
    print("se creo la tabla visionados")

def introducir_visionados():
    conexion = sqlite3.connect("SI.db")
    valores = set()
    while len(valores)<10000:
        id_pelicula = 's'+str(random.randint(1,8809))
        id_usuario = random.randint(1, 30)
        puntuacion = random.uniform(0.0,5.0)
        valores.add((id_pelicula,id_usuario,puntuacion))
    for (id_pelicula,id_usuario,puntuacion) in valores:
        conexion.execute("INSERT OR IGNORE INTO visionados (id_pelicula, id_usuario, puntuacion) VALUES (?, ?, ?)", (id_pelicula, id_usuario, puntuacion))
        conexion.commit()
    print("Entradas creadas")

def graficos():
    # Conectar a la base de datos
    conn = sqlite3.connect('SI.db')

    # Consultar las películas con más visionados
    query2 = '''
    SELECT show.title,CAST(show.duration as integer) AS duration, COUNT(visionados.id_pelicula) AS num_visionados
    FROM show
    JOIN visionados ON show.show_id = visionados.id_pelicula
    WHERE show.type='TV Show'
    GROUP BY show.show_id
    ORDER BY num_visionados DESC
    LIMIT 10
    '''
    query = '''
        SELECT show.title,CAST(show.duration as integer) AS duration, COUNT(visionados.id_pelicula) AS num_visionados
        FROM show
        JOIN visionados ON show.show_id = visionados.id_pelicula
        WHERE show.type='Movie'
        GROUP BY show.show_id
        ORDER BY num_visionados DESC
        LIMIT 10
        '''
    # Leer la consulta en un DataFrame
    df = pd.read_sql_query(query, conn)
    df2 = pd.read_sql_query(query2, conn)
    # Representar en un gráfico de barras
    df.plot(kind='bar', x='title', y='num_visionados', color='green')
    plt.xlabel('Películas')
    plt.ylabel('Número de visionados')
    plt.title('Películas con más visionados')
    plt.show()
    # Representar en un gráfico de barras
    df2.plot(kind='bar', x='title', y='num_visionados', color='green')
    plt.xlabel('Series')
    plt.ylabel('Número de visionados')
    plt.title('Series con más visionados')
    plt.show()

    print(df2.columns)
    df3 = df2[df2['duration']>2]
    y1 = df3['duration'].mean()
    df3 = df2[df2['duration'] <= 2]
    y2 = df3['duration'].mean()
    datos = [y1,y2]
    tipos = ['series largas','series cortas']
    plt.bar(tipos,datos)
    plt.ylabel('Media')
    plt.title('Comparacion medias')
    plt.show()

    df3 = df[df.duration > 90]
    y1 = df3['duration'].mean()
    df3 = df[df.duration <= 90]
    y2 = df3['duration'].mean()
    datos = [y1, y2]
    tipos = ['peliculas largas', 'peliculas cortas']
    plt.bar(tipos, datos)
    plt.ylabel('Media')
    plt.title('Comparacion medias')
    plt.show()

createDataTable()
print()
print("------ APARTADO 2 ------")
num_samples()
med_duracion()
des_duracion()
max_duracion()
min_duracion()
anio()
print()
print("------ APARTADO 3 ------")
print()
f1,f2,f3,f4,f5,f6 = group_dataframe()
print("----- Películas  ----")
print()
info_p(f5)
print()
print("----- Series  ----")
print()
info_p(f6)
print()
print("----- Películas que duran más de 90 minutos o 90 minutos ----")
print()
info_f(f1)
print()
print("----- Películas que duran menos de 90 minutos ----")
print()
info_f(f2)
print()
print("----- Series que duran más de 2 temporadas -----")
print()
info_f(f3)
print()
print("----- Series que duran 2 temporadas o menos -----")
print()
info_f(f4)
print()
print("------ APARTADO 4 y 5 ------")
print()
tabla_usuarios()
tabla_visionados()
#introducir_visionados()
graficos()