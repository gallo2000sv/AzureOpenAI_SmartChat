# Databricks notebook source
# MAGIC %md
# MAGIC # Advanced Email Analysis and Vectorized Search System (V5)

# MAGIC %md
# MAGIC ## 1. Setup and Data Loading

# COMMAND ----------

# Install required libraries
%pip install sentence_transformers scikit-learn

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, udf, lit, when, monotonically_increasing_id, pandas_udf
from pyspark.sql.types import BooleanType, ArrayType, StringType, FloatType, IntegerType
from pyspark.ml.linalg import Vectors, VectorUDT, DenseVector
import re
from sentence_transformers import SentenceTransformer
from sklearn.cluster import MiniBatchKMeans
import pandas as pd
import numpy as np
from typing import Iterator
from pyspark.sql.functions import PandasUDFType

# Azure Storage Configuration
containerstorageaccess = dbutils.secrets.get(scope="your_secret_scope", key="your_secret_key")
storageaccountname = "your_storage_account"
containername = "your_container_name"

spark.conf.set(f"fs.azure.account.key.{storageaccountname}.blob.core.windows.net", containerstorageaccess)

# Mount storage
mount_point = "/mnt/mbox"
if any(mount.mountPoint == mount_point for mount in dbutils.fs.mounts()):
    dbutils.fs.unmount(mount_point)

dbutils.fs.mount(
    source=f"wasbs://{containername}@{storageaccountname}.blob.core.windows.net/",
    mount_point=mount_point,
    extra_configs={f"fs.azure.account.key.{storageaccountname}.blob.core.windows.net": containerstorageaccess}
)

# Load CSV file
csv_file_path = f"{mount_point}/email_data.csv"
spark_df = spark.read.option("header", "true").csv(csv_file_path)
print(f"Data loaded. Number of rows: {spark_df.count()}")

# Save initial DataFrame for reference
spark_df.write.mode("overwrite").saveAsTable("default.emails_raw")


# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Preprocesamiento y Filtrado

# COMMAND ----------

# Verificar si ya existe el DataFrame preprocesado
if spark.catalog.tableExists("default.emails_preprocessed"):
    df_filtered = spark.table("default.emails_preprocessed")
    print("Cargando datos preprocesados existentes.")
else:
    domain_keywords = ['invertir', 'acciones', 'opciones', 'stock options', 'call', 'put', 'forex', 'divisas', 'futuros', 'materias primas', 'swing trading', 'broker', 'estafa', 'asesoría', 'precio', 'servicio']

    @udf(returnType=BooleanType())
    def contains_domain_keywords(text):
        if text is None:
            return False
        return any(keyword in text.lower() for keyword in domain_keywords)

    def preprocess_and_filter(df):
        return df.withColumn("processed_text", 
                             when(col("body").isNotNull(), 
                                  lower(regexp_replace(col("body"), "[^a-zA-Z\\s]", " ")))
                             .otherwise(lit("")))\
                 .filter(contains_domain_keywords(col("processed_text")))

    df_filtered = preprocess_and_filter(spark_df)
    
    # Guardar el DataFrame preprocesado
    df_filtered.write.mode("overwrite").saveAsTable("default.emails_preprocessed")

print(f"Número de correos filtrados: {df_filtered.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Vectorización y Embedding

# COMMAND ----------

# Verificar si ya existe el DataFrame con embeddings
if spark.catalog.tableExists("default.emails_embedded"):
    df_embedded = spark.table("default.emails_embedded")
    print("Cargando embeddings existentes.")
else:
    # Inicializar modelo de embedding
    sentence_model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

    @pandas_udf("array<float>", PandasUDFType.SCALAR_ITER)
    def batch_create_embedding(texts_iter: Iterator[pd.Series]) -> Iterator[pd.Series]:
        for texts in texts_iter:
            embeddings = sentence_model.encode(texts.tolist(), batch_size=32)  # Ajusta batch_size según sea necesario
            yield pd.Series(embeddings.tolist())

    df_embedded = df_filtered.withColumn("embedding", batch_create_embedding("processed_text"))

    # Convertir array de floats a vector
    @udf(returnType=VectorUDT())
    def array_to_vector(arr):
        return DenseVector(arr)

    df_embedded = df_embedded.withColumn("embedding_vector", array_to_vector(col("embedding")))
    
    # Guardar el DataFrame con embeddings
    df_embedded.write.mode("overwrite").saveAsTable("default.emails_embedded")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Identificación de Preguntas

# COMMAND ----------

# Verificar si ya existe el DataFrame con preguntas identificadas
if spark.catalog.tableExists("default.emails_questions"):
    df_questions = spark.table("default.emails_questions")
    print("Cargando preguntas identificadas existentes.")
else:
    question_patterns = r'\b(qué|cómo|cuándo|dónde|por qué|cuál|quién|cuánto)\b|[?]|precio|ganar|invertir|analizar|abrir cuenta|evitar estafa'

    @udf(returnType=BooleanType())
    def identify_question(text):
        if text is None:
            return False
        return bool(re.search(question_patterns, text, re.IGNORECASE))

    df_questions = df_embedded.filter(identify_question(col("processed_text")))
    
    # Guardar el DataFrame con preguntas identificadas
    df_questions.write.mode("overwrite").saveAsTable("default.emails_questions")

print(f"Número de preguntas identificadas: {df_questions.count()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Clustering de Preguntas Similares con MiniBatchKMeans

# COMMAND ----------

# Verificar si ya existe el DataFrame con clusters
if spark.catalog.tableExists("default.emails_clustered"):
    df_clustered = spark.table("default.emails_clustered")
    print("Cargando clusters existentes.")
else:
    def batch_kmeans_clustering(df, num_clusters=20, batch_size=1000):
        embeddings = np.array(df.select("embedding_vector").collect())
        embeddings = np.vstack([e[0] for e in embeddings])
        
        kmeans = MiniBatchKMeans(n_clusters=num_clusters, random_state=42, batch_size=batch_size)
        
        # Procesar en lotes para reducir la carga de memoria
        for i in range(0, len(embeddings), batch_size):
            batch = embeddings[i:i+batch_size]
            kmeans.partial_fit(batch)
        
        labels = kmeans.predict(embeddings)
        return labels

    # Realizar clustering
    num_clusters = min(20, df_questions.count())
    cluster_labels = batch_kmeans_clustering(df_questions, num_clusters)

    # Agregar etiquetas de cluster al DataFrame
    df_questions = df_questions.withColumn("row_id", monotonically_increasing_id())
    cluster_labels_df = spark.createDataFrame([(int(i), int(label)) for i, label in enumerate(cluster_labels)], ["row_id", "cluster"])
    df_clustered = df_questions.join(cluster_labels_df, "row_id").drop("row_id")
    
    # Guardar el DataFrame con clusters
    df_clustered.write.mode("overwrite").saveAsTable("default.emails_clustered")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Extracción de Preguntas y Respuestas Representativas

# COMMAND ----------

# Verificar si ya existen los pares de preguntas y respuestas
if spark.catalog.tableExists("default.qa_pairs"):
    qa_df = spark.table("default.qa_pairs")
    print("Cargando pares de preguntas y respuestas existentes.")
else:
    def extract_qa_pairs(df_clustered):
        qa_pairs = []
        for cluster in range(num_clusters):
            cluster_emails = df_clustered.filter(col("cluster") == cluster)
            if cluster_emails.count() > 0:
                representative_email = cluster_emails.first()
                qa_pairs.append({
                    "cluster": cluster,
                    "question": representative_email["subject"],
                    "answer": representative_email["body"],
                    "freq": cluster_emails.count()
                })
        return spark.createDataFrame(qa_pairs)

    qa_df = extract_qa_pairs(df_clustered)
    
    # Guardar los pares de preguntas y respuestas
    qa_df.write.mode("overwrite").saveAsTable("default.qa_pairs")

display(qa_df.orderBy(col("freq").desc()))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Implementación de Búsqueda Vectorial

# COMMAND ----------

from pyspark.ml.linalg import Vectors
from pyspark.sql.functions import udf, col
from pyspark.sql.types import FloatType
from sentence_transformers import SentenceTransformer
from pyspark.ml.linalg import DenseVector

def vector_search(query, df_with_vectors, top_k=5):
    # Initialize the SentenceTransformer model inside the function
    sentence_model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
    query_embedding = sentence_model.encode([query])[0]  # Encode as batch and take first result
    query_vector = DenseVector(query_embedding)
    
    # Define a UDF to calculate cosine similarity
    @udf(FloatType())
    def cosine_similarity(v):
        return float(v.dot(query_vector) / (Vectors.norm(v, 2) * Vectors.norm(query_vector, 2)))
    
    # Calcular similitud de coseno usando Spark
    df_with_similarity = df_with_vectors.withColumn(
        "similarity",
        cosine_similarity(col("embedding_vector"))
    )
    
    # Obtener los top_k resultados más similares
    top_results = df_with_similarity.orderBy(col("similarity").desc()).limit(top_k)
    return top_results.select("subject", "body", "similarity")

# Ejemplo de uso
query = "¿Cómo puedo empezar a invertir en acciones?"
results = vector_search(query, df_embedded)
display(results)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Almacenamiento y Consulta de Resultados

# COMMAND ----------

# Ejemplo de consulta para obtener las preguntas más frecuentes
top_questions = spark.sql("""
    SELECT cluster, question, freq
    FROM default.qa_pairs
    ORDER BY freq DESC
    LIMIT 10
""")

display(top_questions)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Limpieza Final

# COMMAND ----------

# Desmontar el almacenamiento de blob
dbutils.fs.unmount(mount_point)
print("Almacenamiento desmontado exitosamente")
