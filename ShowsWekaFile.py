import pandas as pd
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('DW.db')

# Consulta para obtener los datos de visualización y usuario_id
query = '''SELECT articulo.type,articulo.country,articulo.release_year,articulo.listed_in,CAST(articulo.duration as 
integer) as duration, COUNT(visualizaciones.show_id) as num_visualizaciones, 
AVG(visualizaciones.avg_rating) as media_usuarios FROM articulo LEFT JOIN visualizaciones ON articulo.show_id = 
visualizaciones.show_id GROUP BY articulo.show_id'''

# Lectura del resultado en un dataframe
df = pd.read_sql(query, conn)

# Convertir valores NaN a strings
df = df.fillna('')
df = df.replace('\n', ' ', regex=True)

# Convertir a un número
df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
df['media_usuarios'] = pd.to_numeric(df['media_usuarios'], errors='coerce').fillna(0)

# Crear columnas para cada tipo de show en listed_in
df['listed_in'] = df['listed_in'].str.strip()
df_listed_in = df['listed_in'].str.get_dummies(', ')
df = pd.concat([df, df_listed_in], axis=1)
df = df.drop('listed_in', axis=1)

# Crear columnas para cada pais en country
df['country'] = df['country'].str.strip()
df_listed_in = df['country'].str.get_dummies(', ')
df = pd.concat([df, df_listed_in], axis=1)
df = df.drop('country', axis=1)

# Añadir atributo class {buena(>7),mala(<4),media(resto)} mediante el rating

df.loc[df['media_usuarios'] > 7, 'class'] = 'buena'
df.loc[df['media_usuarios'] < 4, 'class'] = 'mala'
df.loc[(df['media_usuarios'] >= 4) & (df['media_usuarios'] <= 7), 'class'] = 'media'

df = df.drop('media_usuarios', axis=1)



# Convierte el DataFrame de Pandas a un archivo ARFF
with open('shows_data.arff', 'w', encoding='utf-8') as f:
    f.write('@relation shows_data\n\n')
    # Escribe los nombres de las columnas como atributos
    for col in df.columns:
        if df[col].dtype == 'object':
            unique_values = [str(x) if x is not None else '' for x in set(df[col].tolist())]
            if col == "class":
                f.write('@attribute ' + col + ' {' + ','.join(filter(None, unique_values)) + '}\n')
            else:
                f.write('@attribute "' + col + '" {' + ','.join(filter(None, unique_values)) + '}\n')
        else:
            f.write('@attribute "' + col + '" numeric\n')
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


