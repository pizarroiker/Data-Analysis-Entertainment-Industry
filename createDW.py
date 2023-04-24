import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('DW.db')

# Cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Comando SQL para crear la base de datos y sus tablas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS articulo (
        id           INTEGER NOT NULL,
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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tiempo (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        month INTEGER,
        year  INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipo (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        device VARCHAR(4000)
    )
""")

cursor.execute("""
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

# Construccion tabla tipo
cursor.execute("INSERT INTO tipo (device) VALUES ('movil')")
cursor.execute("INSERT INTO tipo (device) VALUES ('ordenador')")
cursor.execute("INSERT INTO tipo (device) VALUES ('television')")

# Contruccion tabla tiempo
for year in range(2018, 2024):
    for month in range(1, 13):
        cursor.execute("INSERT INTO tiempo (month, year) VALUES (?, ?)", (month, year))

# Cierre de conexión a la base de datos
conn.close()