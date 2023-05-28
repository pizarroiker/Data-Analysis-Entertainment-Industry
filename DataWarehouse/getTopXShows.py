import sqlite3
import pandas as pd

# SQL query to obtain the top X displays of a specific show type
def get_top_x_shows(show_type, x):
    conn = sqlite3.connect('../DDBB/DataWarehouse.db')
    query = f"""
            SELECT s.title, COUNT(*) as num_views
            FROM views v
            JOIN show s ON v.show_id = s.show_id
            WHERE s.type = '{show_type}'
            GROUP BY s.title
            ORDER BY num_views DESC
            LIMIT {x}
        """
    df = pd.read_sql_query(query, conn)
    return df

# Type Selection

tipos = ['Movie','TV Show']
print('Types of audiovisual material available:')
for i, tipo in enumerate(tipos):
    print(f'{i+1}. {tipo}')
tipo = ''
while tipo not in tipos:
    tipo = input('Enter the desired type (Movie or TV Show): ')
    if tipo not in tipos:
        print('Invalid type. Please enter Movie or TV Show.')

# Top Selection

top = int(input('Enter the number of items of the desired top: '))


# We obtain the result of the SLICE & DICE in a
# data frame and print the result

result = get_top_x_shows(tipo, top)
print(result)
