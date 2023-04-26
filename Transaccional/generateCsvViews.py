import csv
import random
import sqlite3
from datetime import date
import numpy as np

# Connection to database

con = sqlite3.connect("SI.db")
cursor = con.cursor()

# Data for further randomization

shows = [row[0] for row in cursor.execute("SELECT show_id FROM show")]
users = [row[0] for row in cursor.execute("SELECT id FROM user")]
start_date = date(2018, 1, 1)
end_date = date(2023, 4, 1)
dates = [date(random.randint(start_date.year, end_date.year),
              random.randint(1, 12),
              1) for _ in range(10100)]
ratings = np.arange(1, 10.1, 0.1).round(1).tolist()

# Adding Random data to rows

rows = []
for i in range(10000):
    show_id = random.choice(shows)
    user_id = random.choice(users)
    date = dates[i]
    rating = random.choice(ratings)
    rows.append([i, show_id, user_id, rating, date])

# Manipulating DATA for later Data Mining

shows = ['s34','s5941','s779','s3686','s8415','s111','s341','s7078','s7803','s7880']
ratings = np.arange(5, 10.1, 0.1).round(1).tolist()

# Adding to rows

for i in range(100):
    id = i+10000
    show_id = random.choice(shows)
    user_id = random.choice(users)
    date = dates[id]
    rating = random.choice(ratings)
    rows.append([id, show_id, user_id, rating, date])

# Building csv with the data in rows

with open('views.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'show_id', 'user_id', 'rating', 'date'])
    writer.writerows(rows)