import pandas as pd
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('DW.db')

# Consulta para obtener los datos de visualización y usuario_id
query = '''
    SELECT articulo.type,articulo.director,articulo.country,articulo.release_year,articulo.duration,articulo.rating, COUNT(visualizaciones.show_id) as num_visualizaciones, AVG(visualizaciones.avg_rating) as media_usuarios
    FROM articulo
    LEFT JOIN visualizaciones ON articulo.show_id = visualizaciones.show_id
    GROUP BY articulo.show_id
'''

# Lectura del resultado en un dataframe
df = pd.read_sql(query, conn)
print(df)

# Convierte el DataFrame de Pandas a un archivo ARFF
with open('wekadata.arff', 'w') as f:
    f.write('@relation nombre_del_archivo\n\n')
    # Escribe los nombres de las columnas como atributos
    for col in df.columns:
        if df[col].dtype == 'object':
            unique_values = list(set(df[col].tolist()))
            if col == "class":
                f.write('@class ' + col + ' {' + ','.join(unique_values) + '}\n')
            else:
                f.write('@attribute ' + col + ' {' + ','.join(unique_values) + '}\n')
        else:
            f.write('@attribute ' + col + ' numeric\n')
    f.write('\n@data\n')
    # Escribe los datos de cada fila en el archivo
    for i, row in df.iterrows():
        values = []
        for col in df.columns:
            if df[col].dtype == 'object':
                values.append("'" + str(row[col]) + "'")
            else:
                values.append(str(row[col]))
        f.write(','.join(values) + '\n')
