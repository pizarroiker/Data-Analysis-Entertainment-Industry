from datetime import datetime
import sqlite3
import pandas as pd

# Connection to the transactional database and to the warehouse
con_dw = sqlite3.connect('../DDBB/DataWarehouse.db')
con_db = sqlite3.connect('../DDBB/TransactionalDatabase.db')

# Cursor to execute SQL commands in both databases
cursor_dw = con_dw.cursor()
cursor_db = con_db.cursor()

# Creation of the item table in the data warehouse

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS articulo (
        show_id      VARCHAR(4000),
        type         VARCHAR(4000),
        title        VARCHAR(4000),
        director     VARCHAR(4000),
        cast         VARCHAR(4000),
        country      VARCHAR(4000),
        date_added   VARCHAR(4000),
        release_year VARCHAR(4000),
        rating       VARCHAR(4000),
        duration     VARCHAR(4000),
        listed_in    VARCHAR(4000),
        description  VARCHAR(4000),
        PRIMARY KEY  (show_id)
    )
""")

# Creation of the user table in the data warehouse

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id           INTEGER,
        name         VARCHAR(4000),
        login_date   DATE,
        country      VARCHAR(4000),
        PRIMARY KEY  (id)
    )
""")

# Creation of the time table in the data warehouse

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS tiempo (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        month INTEGER,
        year  INTEGER,
        UNIQUE (month, year)
    )
""")

# Creation of the fact table (visualizations) in the data warehouse

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS visualizaciones (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        show_id     VARCHAR(2000),
        user_id     INTEGER NOT NULL,
        tiempo_id   INTEGER NOT NULL,
        count       INTEGER,
        avg_rating  NUMBER,
        FOREIGN KEY (show_id) REFERENCES articulo (id),
        FOREIGN KEY (tiempo_id) REFERENCES tiempo (id),
        FOREIGN KEY (user_id) REFERENCES usuario (id)
    )
""")

# Construction time table (JANUARY 2018 - APRIL 2023)

for year in range(2018, 2023):
    for month in range(1, 13):
        cursor_dw.execute("INSERT INTO tiempo (month, year) VALUES (?, ?)", (month, year))

for month in range(1, 5):
    cursor_dw.execute("INSERT INTO tiempo (month, year) VALUES (?, ?)", (month, 2023))

# Users table construction (From the transactional to the storage, we pass the whole table)

query = "SELECT  *  FROM user"
df = pd.read_sql_query(query, con_db)
df.to_sql('usuario',con_dw,if_exists='replace',index=False)

# Construction table items (From the transactional to the storage, we pass the whole table)

query = "SELECT  *  FROM show"
df = pd.read_sql_query(query, con_db)
df.to_sql('articulo',con_dw,if_exists='replace',index=False)

# Construction of fact table (visualizations)

query = "SELECT show_id, user_id, date, COUNT(*) as count, AVG(rating) as avg_rating FROM views GROUP BY show_id, " \
        "user_id, date"
df = pd.read_sql_query(query, con_db)

# Defines the function to calculate the id of the time table based on the date of the display.
def to_time_num(date_str):

    # Convert the date in string to a datetime object
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Obtain the year and month of the date
    year = date.year
    month = date.month

    # Calculate the number of time corresponding to the date
    time_num = (year - 2018) * 12 + month

    return time_num

# Apply the function to the date column and store the results in a new column.

df['date'] = df['date'].apply(to_time_num)

# We rename the column to be able to load the data without problems in the fact table.

df = df.rename(columns={'date': 'tiempo_id'})

# We load the fact table through the dataframe.

df.to_sql('visualizaciones',con_dw,if_exists='replace',index=False)


# Closing database connections

con_dw.close()
con_db.close()