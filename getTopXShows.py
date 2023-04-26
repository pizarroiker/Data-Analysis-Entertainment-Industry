import sqlite3
import pandas as pd

# Consulta SQL para obtener el top X de visualizaciones de un tipo de show específico
def get_top_x_shows(show_type, x):
    conn = sqlite3.connect('DW.db')
    query = f"""
            SELECT s.title, COUNT(*) as num_views
            FROM visualizaciones v
            JOIN articulo s ON v.show_id = s.show_id
            WHERE s.type = '{show_type}'
            GROUP BY s.title
            ORDER BY num_views DESC
            LIMIT {x}
        """
    df = pd.read_sql_query(query, conn)
    return df

# Type Selection

tipos = ['Movie','TV Show']
print('Tipos de material audiovisual disponibles:')
for i, tipo in enumerate(tipos):
    print(f'{i+1}. {tipo}')
tipo = ''
while tipo not in tipos:
    tipo = input('Ingrese el tipo deseado (Movie o TV Show): ')
    if tipo not in tipos:
        print('Tipo inválido. Por favor, ingrese Movie o TV Show.')

# Top Selection

top = int(input('Ingrese el número de elementos del top deseado: '))



result = get_top_x_shows(tipo, top)
print(result)
