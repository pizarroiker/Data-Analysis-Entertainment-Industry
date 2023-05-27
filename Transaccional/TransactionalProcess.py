
import re
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt


def table_show(con):
    df = pd.read_csv("CSV/netflix_titles.csv", sep =';', header=0)
    df.to_sql("show", con, schema = None, if_exists= 'replace', index = False)
    con.commit()

def tabla_users(con):
    df = pd.read_csv("CSV/users.csv", sep=',', header=0)
    df.to_sql("user", con, schema=None, if_exists='replace', index=False)
    con.commit()
def tabla_views(con):
    df = pd.read_csv("CSV/views.csv", sep=',', header=0)
    df.to_sql("views", con, schema=None, if_exists='replace', index=False)
    con.commit()

def group_dataframe(con):
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
def num_samples(con,f):
    frase = "SELECT COUNT(*) FROM show WHERE show_id IS NOT NULL AND type IS NOT NULL AND title IS NOT NULL AND " \
            "director IS NOT NULL AND country NOT NULL AND date_added NOT NULL AND " \
            "release_year NOT NULL AND rating NOT NULL AND duration NOT NULL AND listed_in NOT NULL AND " \
            "description NOT NULL and 'cast' NOT NULL"
    tam = pd.read_sql_query(frase,con).values[0][0]
    f.write("\nNumber of complete samples (without missing values): " + str(tam)+"\n")

def med_duracion(con,f):
    query = "SELECT AVG(duration) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT AVG(duration) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    med_film = pd.read_sql_query(query, con).values[0][0]
    med_show = pd.read_sql_query(query2, con).values[0][0]
    f.write("Average length (movies): " + str(round(med_film))+ " minutes\n")
    f.write("Average length (TV Shows): " + str(round(med_show)) + " seasons\n")

def des_duracion(con,f):
    query = "SELECT AVG(duration * duration) - AVG(duration) * AVG(duration) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT AVG(duration * duration) - AVG(duration) * AVG(duration) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(query, con).values[0][0] ** 0.5
    std_show = pd.read_sql_query(query2, con).values[0][0] ** 0.5
    f.write("Standard deviation of duration (movies): " + str(round(std_film, 2))+"\n")
    f.write("Standard deviation of duration (TV Shows): " + str(round(std_show, 2))+"\n")

def max_duracion(con,f):
    query = "SELECT MAX(CAST(duration as integer)) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT MAX(CAST(duration as integer)) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(query, con).values[0][0]
    std_show = pd.read_sql_query(query2, con).values[0][0]
    f.write("Maximum movie length: " + str(std_film)+ " minutes\n")
    f.write("Maximum TV show length: " + str(std_show) + " seasons\n")

def min_duracion(con,f):
    query = "SELECT MIN(CAST(duration as integer)) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT MIN(CAST(duration as integer)) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(query, con).values[0][0]
    std_show = pd.read_sql_query(query2, con).values[0][0]
    f.write("Minimum movie length: " + str(std_film)+ " minutes\n")
    f.write("Minimum TV show length: " + str(std_show) + " seasons\n")

def year(con,f):
    query = "SELECT MAX(CAST(release_year as integer)) FROM show WHERE release_year IS NOT NULL"
    query2 = "SELECT MIN(CAST(release_year as integer)) FROM show WHERE release_year IS NOT NULL"
    last_year = pd.read_sql_query(query, con).values[0][0]
    first_year = pd.read_sql_query(query2, con).values[0][0]
    f.write("Most recent year of publication: " + str(last_year)+"\n")
    f.write("Oldest year of publication: " + str(first_year)+"\n")

def info_f(d,f):
    f.write("\nLength : "+str(d['duration'].shape[0])+"\n")
    f.write("Median: "+ str(d['duration'].median())+"\n")
    f.write("Mean: " + str(round(d['duration'].mean(), 2))+"\n")
    f.write("Var: " + str(round(d['duration'].var(), 2))+"\n")
    f.write("Maximum: " + str(d['duration'].max())+"\n")
    f.write("Minimum: " + str(d['duration'].min())+"\n")

def info_p(d,f):
    f.write("\nLength : "+str(d['duration'].shape[0])+"\n")
    f.write("Null Values: "+str(d['duration'].isnull().sum())+"\n")
    d['duration'] = d['duration'].dropna().apply(lambda x: re.sub('[^0-9]', '', x)).astype(int)
    f.write("Median: "+ str(d['duration'].median())+"\n")
    f.write("Mean: " + str(round(d['duration'].mean(), 2))+"\n")
    f.write("Var: " + str(round(d['duration'].var(), 2))+"\n")
    f.write("Maximum: " + str(d['duration'].max())+"\n")
    f.write("Minimum: " + str(d['duration'].min())+"\n")


def plots(con):


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

    df = pd.read_sql_query(query, con)
    df2 = pd.read_sql_query(query2, con)

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

if __name__ == "__main__" :
    con = sqlite3.connect("../DDBB/TransactionalDatabase.db")
    table_show(con)
    tabla_users(con)
    tabla_views(con)
    d1, d2, d3, d4, d5, d6 = group_dataframe(con)
    with open('report.txt', 'w') as file:
        file.write("\n------ Duration and age of audiovisual content ------\n")
        num_samples(con,file)
        med_duracion(con,file)
        des_duracion(con,file)
        max_duracion(con,file)
        min_duracion(con,file)
        year(con,file)
        file.write("\n------ Statistical data of each group ------\n")
        file.write("\n------ Movies ------\n")
        info_p(d5,file)
        file.write("\n------ TV Shows ------\n")
        info_p(d6,file)
        file.write("\n----- Movies that are longer than 90 minutes or 90 minutes long ----\n")
        info_f(d1,file)
        file.write("\n----- Movies that last less than 90 minutes ----\n")
        info_f(d2,file)
        file.write("\n----- TV Shows that last more than 2 seasons -----\n")
        info_f(d3,file)
        file.write("\n----- TV Shows that last 2 seasons or less -----\n")
        info_f(d4,file)
    plots(con)
    con.close()