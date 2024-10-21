import os
from fastapi import FastAPI, HTTPException
from databricks import sql
import logging
import time

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/get_data")
async def get_data():
    try:
        logger.info("Intentando conectar a Databricks")
        databricks_host = os.getenv("DATABRICKS_HOST")
        databricks_token = os.getenv("DATABRICKS_TOKEN")
        databricks_http_path = os.getenv("DATABRICKS_HTTP_PATH")
        
        logger.info(f"DATABRICKS_HOST: {databricks_host}")
        logger.info(f"DATABRICKS_HTTP_PATH: {databricks_http_path}")
        logger.info(f"DATABRICKS_TOKEN: {'*' * len(databricks_token) if databricks_token else 'No set'}")

        with sql.connect(
            server_hostname=databricks_host,
            http_path=databricks_http_path,
            access_token=databricks_token
        ) as connection:
            with connection.cursor() as cursor:
                logger.info("Ejecutando consulta SQL")
                start_time = time.time()  # Añadimos esta línea para definir start_time
                cursor.execute("SELECT * FROM default.resultados_notebook LIMIT 10")
                result = cursor.fetchall()
                end_time = time.time()
                logger.info(f"Consulta SQL completada en {end_time - start_time:.2f} segundos")
                columns = [desc[0] for desc in cursor.description]

        logger.info(f"Datos obtenidos: {len(result)} filas")
        return {"columns": columns, "data": result}
        #logger.info("Datos obtenidos exitosamente")
        #return {"columns": columns, "data": result}
    except Exception as e:
        logger.error(f"Error al obtener datos de Databricks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    return response

@app.get("/env-check")
async def env_check():
       return {
           "DATABRICKS_HOST": os.getenv("DATABRICKS_HOST"),
           "DATABRICKS_HTTP_PATH": os.getenv("DATABRICKS_HTTP_PATH"),
           "DATABRICKS_TOKEN": os.getenv("DATABRICKS_TOKEN", "")[:5] + "..." if os.getenv("DATABRICKS_TOKEN") else None
       }
