import pandas as pd
import sqlite3
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier
from weka.classifiers import Evaluation

# Conexión a la base de datos
conn = sqlite3.connect('DW.db')

# Consulta para obtener los datos de visualización y usuario_id
query = '''
    SELECT usuarios.*, COUNT(visualizaciones.usuario_id) as num_visualizaciones, AVG(visualizaciones.valoracion) as media_valoraciones
    FROM usuarios
    LEFT JOIN visualizaciones ON usuarios.usuario_id = visualizaciones.usuario_id
    GROUP BY usuarios.usuario_id
'''

# Lectura del resultado en un dataframe
df_usuario = pd.read_sql(query, conn)
df_usuario.to_csv('wekadata.csv', index=False)

# Iniciar JVM de WEKA
jvm.start()

# Cargar datos desde archivo CSV
loader = Loader(classname="weka.core.converters.CSVLoader")
data = loader.load_file("usuarios_visualizaciones.csv")
data.class_is_last()

# Dividir los datos en conjuntos de entrenamiento y prueba
train_data = data.train_cv(10, 0)
test_data = data.test_cv(10, 0)

# Construir modelo de clasificación usando J48
classifier = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.25"])
classifier.build_classifier(train_data)

# Evaluar el modelo utilizando los datos de prueba
eval = Evaluation(train_data)
eval.evaluate_model(classifier, test_data)

# Imprimir resultados
print(eval.summary())
print(eval.class_details())
print(eval.confusion_matrix)