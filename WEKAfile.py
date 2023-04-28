import pandas as pd
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('DW.db')

# Consulta para obtener los datos de visualización y usuario_id
query = '''
    SELECT usuario.*, COUNT(visualizaciones.user_id) as num_visualizaciones, AVG(visualizaciones.avg_rating) as media_valoraciones
    FROM usuario
    LEFT JOIN visualizaciones ON usuario.id = visualizaciones.user_id
    GROUP BY usuario.id
'''

# Lectura del resultado en un dataframe
df_usuario = pd.read_sql(query, conn)
df_usuario.to_csv('wekadata.csv', index=False)

df = pd.read_csv('wekadata.csv')
with open('wekadata.arff', 'w') as f:
    f.write('@relation wekadata\n\n')
    # Escribe los nombres de las columnas como atributos
    for col in df.columns:
        f.write('@attribute ' + col + ' numeric\n')
    f.write('\n@data\n')
    # Escribe los datos de cada fila en el archivo
    for i, row in df.iterrows():
        f.write(','.join([str(x) for x in row.values]) + '\n')
