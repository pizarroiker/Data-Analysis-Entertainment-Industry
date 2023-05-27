
import re
import sqlite3
import pandas as pd
from matplotlib import pyplot as plt

#Creates Shows Table
def table_show(con):
    df = pd.read_csv("CSV/netflix_titles.csv", sep =';', header=0)
    df.to_sql("show", con, schema = None, if_exists= 'replace', index = False)
    con.commit()

#Creates Users Table
def tabla_users(con):
    df = pd.read_csv("CSV/users.csv", sep=',', header=0)
    df.to_sql("user", con, schema=None, if_exists='replace', index=False)
    con.commit()

#Creates Views Table
def tabla_views(con):
    df = pd.read_csv("CSV/views.csv", sep=',', header=0)
    df.to_sql("views", con, schema=None, if_exists='replace', index=False)
    con.commit()

#Split Shows Table into Dataframes (TV Series, Shows, TV Series 2 or less seasons, TV Series 3 or more seasons....)
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

# Writes on the file the number of samples without missing values
def num_samples(con,f):
    frase = "SELECT COUNT(*) FROM show WHERE show_id IS NOT NULL AND type IS NOT NULL AND title IS NOT NULL AND " \
            "director IS NOT NULL AND country NOT NULL AND date_added NOT NULL AND " \
            "release_year NOT NULL AND rating NOT NULL AND duration NOT NULL AND listed_in NOT NULL AND " \
            "description NOT NULL and 'cast' NOT NULL"
    tam = pd.read_sql_query(frase,con).values[0][0]
    f.write("<tr>\n <td>Number of complete samples (without missing values)</td>\n <td>"+str(tam)+"</td>\n </tr>\n")

# Writes on the file the average duration of TV shows and movies
def med_duration(con,f):
    query = "SELECT AVG(duration) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT AVG(duration) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    med_film = pd.read_sql_query(query, con).values[0][0]
    med_show = pd.read_sql_query(query2, con).values[0][0]
    f.write("<tr>\n <td>Average duration (Movies)</td>\n <td>" + str(round(med_film))+ " minutes" + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Average duration (TV Shows)</td>\n <td>" + str(round(med_show)) + " seasons" + "</td>\n </tr>\n")

# Writes on the file the standard deviation of duration from TV shows and movies
def des_duration(con,f):
    query = "SELECT AVG(duration * duration) - AVG(duration) * AVG(duration) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT AVG(duration * duration) - AVG(duration) * AVG(duration) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(query, con).values[0][0] ** 0.5
    std_show = pd.read_sql_query(query2, con).values[0][0] ** 0.5
    f.write("<tr>\n <td>Standard deviation of duration (Movies)</td>\n <td>" + str(round(std_film, 2)) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Standard deviation of duration (TV Shows)</td>\n <td>" + str(round(std_show, 2)) + "</td>\n </tr>\n")

# Writes on the file the maximum duration of TV shows and movies
def max_duration(con,f):
    query = "SELECT MAX(CAST(duration as integer)) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT MAX(CAST(duration as integer)) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(query, con).values[0][0]
    std_show = pd.read_sql_query(query2, con).values[0][0]
    f.write("<tr>\n <td>Maximum Movie duration</td>\n <td>" + str(std_film)+ " minutes" + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Maximum TV show duration</td>\n <td>" + str(std_show)+ " seasons" + "</td>\n </tr>\n")

# Writes on the file the minimum duration of TV shows and movies
def min_duration(con,f):
    query = "SELECT MIN(CAST(duration as integer)) FROM show WHERE type = 'Movie' AND duration IS NOT NULL"
    query2 = "SELECT MIN(CAST(duration as integer)) FROM show WHERE type = 'TV Show' AND duration IS NOT NULL"
    std_film = pd.read_sql_query(query, con).values[0][0]
    std_show = pd.read_sql_query(query2, con).values[0][0]
    f.write("<tr>\n <td>Minimum Movie duration</td>\n <td>" + str(std_film) + " minutes" + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Minimum TV show duration</td>\n <td>" + str(std_show) + " seasons" + "</td>\n </tr>\n")

# Writes on the file the oldest and the most recent year of publication
def year(con,f):
    query = "SELECT MAX(CAST(release_year as integer)) FROM show WHERE release_year IS NOT NULL"
    query2 = "SELECT MIN(CAST(release_year as integer)) FROM show WHERE release_year IS NOT NULL"
    last_year = pd.read_sql_query(query, con).values[0][0]
    first_year = pd.read_sql_query(query2, con).values[0][0]
    f.write("<tr>\n <td>Most recent year of publication</td>\n <td>" + str(last_year) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Oldest year of publication</td>\n <td>" + str(first_year) +"</td>\n </tr>\n")

# Writes on the file statistical data of the dataframe duration
def info_f(d,f):
    f.write("<table>\n<tr>\n<th>Statistic</th>\n<th>Value</th>\n</tr>\n")
    f.write("<tr>\n <td>Length</td>\n <td>" + str(d['duration'].shape[0]) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Median</td>\n <td>" + str(d['duration'].median()) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Mean</td>\n <td>" + str(round(d['duration'].mean(), 2)) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Var</td>\n <td>" + str(round(d['duration'].var(), 2)) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Maximum</td>\n <td>" + str(d['duration'].max()) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Minimum</td>\n <td>" + str(d['duration'].min()) + "</td>\n </tr>\n")
    f.write("</table>\n")

# Writes on the file statistical data of the dataframe duration including null values count
def info_p(d,f):
    f.write("<table>\n<tr>\n<th>Statistic</th>\n<th>Value</th>\n</tr>\n")
    f.write("<tr>\n <td>Length</td>\n <td>" + str(d['duration'].shape[0]) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Null Values</td>\n <td>" + str(d['duration'].isnull().sum()) + "</td>\n </tr>\n")
    d['duration'] = d['duration'].dropna().apply(lambda x: re.sub('[^0-9]', '', x)).astype(int)
    f.write("<tr>\n <td>Median</td>\n <td>" + str(d['duration'].median()) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Mean</td>\n <td>" + str(round(d['duration'].mean(), 2)) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Var</td>\n <td>" + str(round(d['duration'].var(), 2)) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Maximum</td>\n <td>" + str(d['duration'].max()) + "</td>\n </tr>\n")
    f.write("<tr>\n <td>Minimum</td>\n <td>" + str(d['duration'].min()) + "</td>\n </tr>\n")
    f.write("</table>\n")

# Creates the plots
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

# MAIN
if __name__ == "__main__" :
    # Connect to database
    con = sqlite3.connect("../DDBB/TransactionalDatabase.db")
    # Create database
    table_show(con)
    tabla_users(con)
    tabla_views(con)
    # Split into dataframes
    d1, d2, d3, d4, d5, d6 = group_dataframe(con)
    # Create the report
    html_start = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }
    h1 {
    text-align: center;
    color: #333;
    }

    table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    }

    table, th, td {
    border: 1px solid #333;
    padding: 8px;
    }

    th {
    background-color: #333;
    color: #fff;
    }

    </style>
    </head>
    <body>
    '''
    html_end= ''' 
    </body>
    </html>
    '''
    with open('report.html', 'w') as file:
        file.write(html_start)
        file.write("\n<h1>Duration and age of audiovisual content</h1>\n")
        file.write("<table>\n <tr>\n <th>Statistic</th>\n <th>Result</th>\n </tr>\n")
        num_samples(con,file)
        med_duration(con,file)
        des_duration(con,file)
        max_duration(con,file)
        min_duration(con,file)
        year(con,file)
        file.write("</table>\n")
        file.write("<h1>Statistical data of each group</h1>\n")
        file.write("<h2>Movies</h2>\n")
        info_p(d5,file)
        file.write("<h2>TV Shows</h2>\n")
        info_p(d6,file)
        file.write("<h2> Movies that are longer than 90 minutes or 90 minutes long</h2>\n")
        info_f(d1,file)
        file.write("<h2> Movies that last less than 90 minutes</h2>\n")
        info_f(d2,file)
        file.write("<h2> TV Shows that last more than 2 seasons</h2>\n")
        info_f(d3,file)
        file.write("<h2> TV Shows that last 2 seasons or less</h2>\n")
        info_f(d4,file)
        file.write(html_end)
    # Create the plots
    plots(con)
    # Close Connection
    con.close()