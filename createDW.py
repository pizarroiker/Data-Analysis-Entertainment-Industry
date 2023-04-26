import sqlite3

import pandas as pd

# Conexión a la base de datos transaccional y al almacen
con_dw = sqlite3.connect('DW.db')
con_db = sqlite3.connect('DB.db')

# Cursor para ejecutar comandos SQL en ambos
cursor_dw = con_dw.cursor()
cursor_db = con_db.cursor()

# Creación de la tabla artículo en el almacen de datos

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS articulo (
        id           VARCHAR(4000),
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
        PRIMARY KEY  (id)
    )
""")

# Creación de la tabla usuario en el almacen de datos

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id           INTEGER,
        nombre         VARCHAR(4000),
        fecha_inicio        DATE,
        pais            VARCHAR(4000),
        PRIMARY KEY  (id)
    )
""")

# Creación de la tabla tiempo en el almacen de datos

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS tiempo (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        month INTEGER,
        year  INTEGER
    )
""")

# Creación de la tabla de hechos (visualizaciones) en el almacen de datos

cursor_dw.execute("""
    CREATE TABLE IF NOT EXISTS visualizaciones (
        id          INTEGER NOT NULL,
        tiempo_id   INTEGER NOT NULL,
        tipo_id     INTEGER NOT NULL,
        articulo_id INTEGER NOT NULL,
        amount      NUMBER,
        PRIMARY KEY (id),
        FOREIGN KEY (articulo_id) REFERENCES articulo (id),
        FOREIGN KEY (tiempo_id) REFERENCES tiempo (id),
        FOREIGN KEY (tipo_id) REFERENCES tipo (id)
    )
""")

# Contrucción tabla tiempo

for year in range(2018, 2024):
    for month in range(1, 13):
        cursor_dw.execute("INSERT INTO tiempo (month, year) VALUES (?, ?)", (month, year))

# Contrucción tabla usuarios

query = "SELECT  *  FROM user"
f1 = pd.read_sql_query(query, con_db)
for _ in f1:
    cursor_dw.execute("INSERT INTO usuario (id, nombre, fecha_inicio, pais) VALUES (?, ?, ?, ?)",_)

# Contrucción tabla artículos

#cursor_db.execute("SELECT  *  FROM show")

# Cierre de conexiones a las bases de datos

con_dw.close()
con_db.close()