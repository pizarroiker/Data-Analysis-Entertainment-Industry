import pandas as pd
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('DW.db')

# Consulta para obtener los datos de visualización y usuario_id
query = '''
    SELECT usuario.id, usuario.country, COUNT(visualizaciones.user_id) as num_visualizaciones, AVG(visualizaciones.avg_rating) as media_valoraciones
    FROM usuario
    LEFT JOIN visualizaciones ON usuario.id = visualizaciones.user_id
    GROUP BY usuario.id
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
            if col == "country":
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
