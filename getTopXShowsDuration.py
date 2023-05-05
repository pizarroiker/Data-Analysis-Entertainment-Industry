import sqlite3
import pandas as pd

# Consulta SQL para obtener el top X de visualizaciones de un tipo de show y duracion específicos
def get_top_x_shows(show_type, x, duration):
    conn = sqlite3.connect('DW.db')
    if show_type == 'Movie':
        query = f"""
                SELECT s.title, COUNT(*) as num_views
                FROM visualizaciones v
                JOIN articulo s ON v.show_id = s.show_id
                WHERE s.type = '{show_type}'
                AND CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) {'>' if duration == 'Over 90 min' else '<='} 90
                GROUP BY s.title
                ORDER BY num_views DESC
                LIMIT {x}
            """
    elif show_type == 'TV Show':
        seasons = {'1': 1, '2': 2, '3': 3}
        num_seasons = seasons[duration]
        query = f"""
                SELECT s.title, COUNT(*) as num_views
                FROM visualizaciones v
                JOIN articulo s ON v.show_id = s.show_id
                WHERE s.type = '{show_type}'
                AND CAST(SUBSTR(duration, 1, INSTR(duration, ' ') - 1) AS INTEGER) {'=' if num_seasons <= 2 else '>='} {num_seasons}
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

# Duration Selection

duration = ''
if tipo == 'Movie':
        while duration not in ['Over 90 min', 'Less or equal to 90 min']:
            duration = input('¿Desea incluir películas con duración mayor a 90 minutos? (s/n): ')
            if duration.lower() == 's':
                duration = 'Over 90 min'
            elif duration.lower() == 'n':
                duration = 'Less or equal to 90 min'
            else:
                print('Respuesta inválida. Por favor, ingrese s o n.')
elif tipo == 'TV Show':
        while duration not in ['1', '2', '3']:
            print()
            print('Advertencia: El 3 busca las series con 3 o más temporadas.')
            duration = input('¿Cuántas temporadas desea incluir? (1, 2, 3): ')
            if duration not in ['1', '2', '3']:
                print('Respuesta inválida. Por favor, ingrese 1, 2 o 3+.')


# Obtenemos el resultado del SLICE & DICE en un
# data frame e imprimimos el resultado

result = get_top_x_shows(tipo, top, duration)
print(result)

