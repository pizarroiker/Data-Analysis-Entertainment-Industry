import csv
import random
from datetime import datetime, timedelta

# Generar 1000 filas de datos aleatorios
rows = []
for i in range(10000):
    # Generar un ID único
    id = i + 1

    # Generar un nombre aleatorio
    name = f"User {id}"

    # Generar una fecha de inicio de sesión aleatoria en los últimos 30 días
    last_login = datetime.now() - timedelta(days=random.randint(0, 30))

    # Agregar la fila a la lista de filas
    rows.append([id, name, last_login])

# Escribir los datos en un archivo CSV
with open("datos.csv", "w", newline="") as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(["id", "Nombre", "Ultima Fecha de Inicio de Sesion"])
    writer.writerows(rows)