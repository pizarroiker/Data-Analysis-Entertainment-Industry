import csv
import random
from datetime import datetime, timedelta

countries = ["Spain", "Germany", "France", "Japan", "USA"]
# Generate 1000 rows of random data
rows = []
for i in range(300):
    # Generate a unique ID
    id = i + 1

    # Generate a random name
    name = f"User {id}"

    # Generate a random login date in the last 30 days
    last_login = datetime.now() - timedelta(days=random.randint(0, 30))

    country = random.choice(countries)

    # Add the row to the row list
    rows.append([id, name, last_login, country])

# Write data to a CSV file
with open("users.csv", "w", newline="") as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(["id", "name", "login_date","country"])
    writer.writerows(rows)