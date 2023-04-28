import sqlite3
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances

# Carga los datos de usuarios y visualizaciones desde la base de datos
conn = sqlite3.connect('DW.db')
df_visualizaciones = pd.read_sql_query("SELECT * FROM visualizaciones", conn)

# Crea la matriz de usuarios por elementos vistos (Usamos la operación OLAP Pivot)
matriz_usuarios_elementos = pd.pivot_table(df_visualizaciones, values='avg_rating', index='user_id', columns='show_id')

def recomendar_programas(usuario, matriz_usuarios_elementos, n):

    # Calcula la similitud del coseno entre los usuarios
    matriz_usuarios_elementos = matriz_usuarios_elementos.fillna(0)
    similitud_usuarios = 1 - pairwise_distances(matriz_usuarios_elementos, metric='euclidean')

    # Encuentra los usuarios más similares
    indices_usuarios = matriz_usuarios_elementos.index
    indice_usuario = np.where(indices_usuarios == usuario)[0][0]
    similitudes = list(zip(indices_usuarios, similitud_usuarios[indice_usuario]))
    similitudes.sort(key=lambda x: x[1], reverse=True)
    usuarios_similares = [similitud[0] for similitud in similitudes[1:]]

    # Encuentra los elementos que el usuario ha visto
    elementos_vistos = matriz_usuarios_elementos.loc[usuario]
    elementos_vistos = elementos_vistos[~(elementos_vistos == 0)].index

    # Encuentra los elementos que los usuarios similares han visto pero el usuario no ha visto
    recomendaciones = {}
    for usuario_similar in usuarios_similares:
        elementos_vistos_similar = matriz_usuarios_elementos.loc[usuario_similar]
        elementos_vistos_similar = elementos_vistos_similar[~(elementos_vistos_similar == 0)].index
        elementos_no_vistos = set(elementos_vistos_similar) - set(elementos_vistos)
        for elemento in elementos_no_vistos:
            if elemento in recomendaciones:
                recomendaciones[elemento] += similitudes[usuarios_similares.index(usuario_similar)][1]
            else:
                recomendaciones[elemento] = similitudes[usuarios_similares.index(usuario_similar)][1]

    # Ordena las recomendaciones por similitud y devuelve las primeras n
    recomendaciones_ordenadas = sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)[:n]
    return [recomendacion[0] for recomendacion in recomendaciones_ordenadas]


# Pide al usuario que ingrese los datos de entrada
user = int(input('Ingrese el ID del usuario: '))
while user <= 0 or user > 300:
    user = int(input('El ID del usuario debe estar entre 1 y 300. Ingrese nuevamente: '))

x = int(input('Ingrese el número de elementos a recomendar (máximo 10): '))
while x <= 0 or x > 10:
    x = int(input('El número de elementos a recomendar debe estar entre 1 y 10. Ingrese nuevamente: '))

# Obtiene las recomendaciones y las imprime en pantalla
recomendaciones = recomendar_programas(user, matriz_usuarios_elementos, x)
sql_query = "SELECT title FROM articulo WHERE show_id IN ({})".format(','.join("'" + s + "'" for s in recomendaciones))
df_recomendaciones = pd.read_sql_query(sql_query, conn)
print(df_recomendaciones)