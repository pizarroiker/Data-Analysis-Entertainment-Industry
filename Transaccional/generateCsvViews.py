import csv
import random
import sqlite3
from datetime import date, timedelta

import numpy as np

con = sqlite3.connect("SI.db")
cursor = con.cursor()

# Generar lista de películas y usuarios
shows = [row[0] for row in cursor.execute("SELECT show_id FROM show")]
users = [row[0] for row in cursor.execute("SELECT id FROM user")]

# Generar lista de fechas
start_date = date(2018, 1, 1)
end_date = date(2023, 4, 1) # Modificado para incluir abril 2023
dates = [date(random.randint(start_date.year, end_date.year),
              random.randint(1, 12), # Generar mes aleatorio
              1) for _ in range(10000)]

# Generar lista de puntuaciones posibles
ratings = np.arange(1, 10.1, 0.1).round(1).tolist()

# Generar entradas semi-aleatorias
rows = []
for i in range(10000):
    show_id = random.choice(shows)
    user_id = random.choice(users)
    date = dates[i]
    rating = random.choice(ratings)
    rows.append([None, show_id, user_id, rating, date])

# Escribir a un archivo CSV
with open('views.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'show_id', 'user_id', 'rating', 'date'])
    writer.writerows(rows)