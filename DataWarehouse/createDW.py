from datetime import datetime
import sqlite3
import pandas as pd

# Conexión a la base de datos transaccional y al almacen
con_dw = sqlite3.connect('../DDBB/DataWarehouse.db')
con_db = sqlite3.connect('../DDBB/TransactionalDatabase.db')

# Cursor para ejecutar comandos SQL en ambos
cursor_dw = con_dw.cursor()
cursor_db = con_db.cursor()

# Creación de la tabla artículo en el almacén de datos

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

# Creación de la tabla usuario en el almacén de datos

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id           INTEGER,
        name         VARCHAR(4000),
        login_date   DATE,
        country      VARCHAR(4000),
        PRIMARY KEY  (id)
    )
""")

# Creación de la tabla tiempo en el almacén de datos

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS tiempo (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        month INTEGER,
        year  INTEGER,
        UNIQUE (month, year)
    )
""")

# Creación de la tabla de hechos (visualizaciones) en el almacén de datos

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

# Contrucción tabla tiempo (ENERO 2018 - ABRIL 2023)

for year in range(2018, 2023):
    for month in range(1, 13):
        cursor_dw.execute("INSERT INTO tiempo (month, year) VALUES (?, ?)", (month, year))

for month in range(1, 5):
    cursor_dw.execute("INSERT INTO tiempo (month, year) VALUES (?, ?)", (month, 2023))

# Contrucción tabla usuarios (Desde el transaccional al almacen, pasamos la tabla entera)

query = "SELECT  *  FROM user"
df = pd.read_sql_query(query, con_db)
df.to_sql('usuario',con_dw,if_exists='replace',index=False)

# Contrucción tabla artículos (Desde el transaccional al almacen, pasamos la tabla entera)

query = "SELECT  *  FROM show"
df = pd.read_sql_query(query, con_db)
df.to_sql('articulo',con_dw,if_exists='replace',index=False)

# Contrucción tabla de hechos (visualizaciones)

query = "SELECT show_id, user_id, date, COUNT(*) as count, AVG(rating) as avg_rating FROM views GROUP BY show_id, " \
        "user_id, date"
df = pd.read_sql_query(query, con_db)

# Define la función para calcular el id de la tabla tiempo en base a la fecha de la visualización
def to_time_num(date_str):

    # Convertir la fecha en string a un objeto datetime
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Obtener el año y mes de la fecha
    year = date.year
    month = date.month

    # Calcular el número de tiempo correspondiente a la fecha
    time_num = (year - 2018) * 12 + month

    return time_num
# FIN FUNCION

# Aplica la función a la columna de fechas y almacena los resultados en una nueva columna

df['date'] = df['date'].apply(to_time_num)

# Renombramos la columna para poder cargar los datos sin problemas en la tabla de hechos

df = df.rename(columns={'date': 'tiempo_id'})

# Cargamos mediante el dataframe la tabla de hechos

df.to_sql('visualizaciones',con_dw,if_exists='replace',index=False)


# Cierre de conexiones a las bases de datos

con_dw.close()
con_db.close()