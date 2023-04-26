
import re
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt


def createDataTable():
    con = sqlite3.connect("SI.db")
    df = pd.read_csv("netflix_titles.csv", sep =';', header=0)
    df.to_sql("show", con, schema = None, if_exists= 'replace', index = False)
    con.commit()

def num_samples():
    con = sqlite3.connect("SI.db")
    frase = "SELECT COUNT(*) FROM show WHERE show_id IS NOT NULL AND type IS NOT NULL AND title IS NOT NULL AND " \
            "director IS NOT NULL AND country NOT NULL AND date_added NOT NULL AND " \
            "release_year NOT NULL AND rating NOT NULL AND duration NOT NULL AND listed_in NOT NULL AND " \
            "description NOT NULL and 'cast' NOT NULL"
    tam = pd.read_sql_query(frase,con).values[0][0]
    print("Number of complete samples (without missing values): " + str(tam))

def med_duracion():
    con = sqlite3.connect("SI.db")
    query = "SELECT AVG(duration) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT AVG(duration) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    med_film = pd.read_sql_query(query, con).values[0][0]
    med_show = pd.read_sql_query(query2, con).values[0][0]
    print("Average length (movies): " + str(round(med_film))+ " minutes")
    print("Average length (TV Shows): " + str(round(med_show)) + " seasons")

def des_duracion():
    con = sqlite3.connect("SI.db")
    query = "SELECT AVG(duration * duration) - AVG(duration) * AVG(duration) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT AVG(duration * duration) - AVG(duration) * AVG(duration) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(query, con).values[0][0] ** 0.5
    std_show = pd.read_sql_query(query2, con).values[0][0] ** 0.5
    print("Standard deviation of duration (movies): " + str(round(std_film, 2)))
    print("Standard deviation of duration (TV Shows): " + str(round(std_show, 2)))

def max_duracion():
    con = sqlite3.connect("SI.db")
    query = "SELECT MAX(CAST(duration as integer)) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT MAX(CAST(duration as integer)) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(query, con).values[0][0]
    std_show = pd.read_sql_query(query2, con).values[0][0]
    print("Maximum movie length: " + str(std_film)+ " minutes")
    print("Maximum TV show length: " + str(std_show) + " seasons")

def min_duracion():
    con = sqlite3.connect("SI.db")
    query = "SELECT MIN(CAST(duration as integer)) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT MIN(CAST(duration as integer)) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(query, con).values[0][0]
    std_show = pd.read_sql_query(query2, con).values[0][0]
    print("Minimum movie length: " + str(std_film)+ " minutes")
    print("Minimum TV show length: " + str(std_show) + " seasons")

def year():
    con = sqlite3.connect("SI.db")
    query = "SELECT MAX(CAST(release_year as integer)) FROM show WHERE release_year IS NOT NULL"
    query2 = "SELECT MIN(CAST(release_year as integer)) FROM show WHERE release_year IS NOT NULL"
    last_year = pd.read_sql_query(query, con).values[0][0]
    first_year = pd.read_sql_query(query2, con).values[0][0]
    print("Most recent year of publication: " + str(last_year))
    print("Oldest year of publication: " + str(first_year))

def group_dataframe():
    con = sqlite3.connect("SI.db")
    query = "SELECT  * FROM show WHERE type = 'Movie' AND CAST(duration as integer) >= 90 "
    query2 = "SELECT  *  FROM show WHERE type = 'Movie' AND CAST(duration as integer) < 90 "
    query3 = "SELECT  *  FROM show WHERE type = 'TV Show' AND CAST(duration as integer) > 2 "
    query4 = "SELECT * FROM show WHERE type = 'TV Show' AND CAST(duration as integer) <= 2 "
    query5 = "SELECT  *  FROM show WHERE type = 'Movie'"
    query6 = "SELECT  *  FROM show WHERE type = 'TV Show'"
    f1 = pd.read_sql_query(query, con)
    f2 = pd.read_sql_query(query2, con)
    f3 = pd.read_sql_query(query3, con)
    f4 = pd.read_sql_query(query4, con)
    f5 = pd.read_sql_query(query5, con)
    f6 = pd.read_sql_query(query6, con)
    f1['duration'] = f1['duration'].apply(lambda x: re.sub('[^0-9]','',x)).astype(int)
    f2['duration'] = f2['duration'].apply(lambda x: re.sub('[^0-9]','', x)).astype(int)
    f3['duration'] = f3['duration'].apply(lambda x: re.sub('[^0-9]','', x)).astype(int)
    f4['duration'] = f4['duration'].apply(lambda x: re.sub('[^0-9]','', x)).astype(int)
    return f1,f2,f3,f4,f5,f6

def info_f(f):
    print("Length : "+str(f['duration'].shape[0]))
    print("Median: "+ str(f['duration'].median()))
    print("Mean: " + str(round(f['duration'].mean(), 2)))
    print("Var: " + str(round(f['duration'].var(), 2)))
    print("Maximum: " + str(f['duration'].max()))
    print("Minimum: " + str(f['duration'].min()))

def info_p(f):
    print("Length : "+str(f['duration'].shape[0]))
    print("Null Values: "+str(f['duration'].isnull().sum()))
    f['duration'] = f['duration'].dropna().apply(lambda x: re.sub('[^0-9]', '', x)).astype(int)
    print("Median: "+ str(f['duration'].median()))
    print("Mean: " + str(round(f['duration'].mean(), 2)))
    print("Var: " + str(round(f['duration'].var(), 2)))
    print("Maximum: " + str(f['duration'].max()))
    print("Minimum: " + str(f['duration'].min()))

def tabla_usuarios():
    con = sqlite3.connect("SI.db")
    df = pd.read_csv("users.csv", sep=',', header=0)
    df.to_sql("user", con, schema=None, if_exists='replace', index=False)
    con.commit()
def tabla_visionados():
    con = sqlite3.connect("SI.db")
    df = pd.read_csv("views.csv", sep=',', header=0)
    df.to_sql("views", con, schema=None, if_exists='replace', index=False)
    con.commit()

def plots():

    conn = sqlite3.connect('SI.db')


    query2 = '''
    SELECT show.title,CAST(show.duration as integer) AS duration, COUNT(views.show_id) AS num_views
    FROM show
    JOIN views ON show.show_id = views.show_id
    WHERE show.type='TV Show'
    GROUP BY show.show_id
    ORDER BY num_views DESC
    LIMIT 10
    '''
    query = '''
        SELECT show.title,CAST(show.duration as integer) AS duration, COUNT(views.show_id) AS num_views
        FROM show
        JOIN views ON show.show_id = views.show_id
        WHERE show.type='Movie'
        GROUP BY show.show_id
        ORDER BY num_views DESC
        LIMIT 10
        '''

    df = pd.read_sql_query(query, conn)
    df2 = pd.read_sql_query(query2, conn)

    df.plot(kind='bar', x='title', y='num_views', color='green')
    plt.xlabel('Movies')
    plt.ylabel('Number of views')
    plt.title('Movies with the most views')
    plt.show()

    df2.plot(kind='bar', x='title', y='num_views', color='green')
    plt.xlabel('TV Shows')
    plt.ylabel('Number of views')
    plt.title('TV Shows with the most views')
    plt.show()

    print(df2.columns)
    df3 = df2[df2['duration']>2]
    y1 = df3['duration'].mean()
    df3 = df2[df2['duration'] <= 2]
    y2 = df3['duration'].mean()
    datos = [y1,y2]
    tipos = ['Long TV Shows','Short TV Shows']
    plt.bar(tipos,datos)
    plt.ylabel('Average')
    plt.title('Comparison of averages')
    plt.show()

    df3 = df[df.duration > 90]
    y1 = df3['duration'].mean()
    df3 = df[df.duration <= 90]
    y2 = df3['duration'].mean()
    datos = [y1, y2]
    tipos = ['Long Movies', 'Short Movies']
    plt.bar(tipos, datos)
    plt.ylabel('Average')
    plt.title('Comparison of averages')
    plt.show()

createDataTable()
print()
print("------ APARTADO 2 ------")
num_samples()
med_duracion()
des_duracion()
max_duracion()
min_duracion()
year()
print()
print("------ APARTADO 3 ------")
print()
f1,f2,f3,f4,f5,f6 = group_dataframe()
print("----- Movies  ----")
print()
info_p(f5)
print()
print("----- TV Shows  ----")
print()
info_p(f6)
print()
print("----- Movies that are longer than 90 minutes or 90 minutes long ----")
print()
info_f(f1)
print()
print("----- Movies that last less than 90 minutes ----")
print()
info_f(f2)
print()
print("----- TV Shows that last more than 2 seasons -----")
print()
info_f(f3)
print()
print("----- TV Shows that last 2 seasons or less -----")
print()
info_f(f4)
print()
print("------ APARTADO 4 y 5 ------")
print()
tabla_usuarios()
tabla_visionados()
plots()