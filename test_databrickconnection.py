import os
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.jobs.api import JobsApi

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
print(f"DATABRICKS_HOST: {DATABRICKS_HOST}")
print(f"DATABRICKS_TOKEN: {'*' * len(DATABRICKS_TOKEN) if DATABRICKS_TOKEN else 'No set'}")

def test_databricks_connection():
    try:
        api_client = ApiClient(host=DATABRICKS_HOST, token=DATABRICKS_TOKEN)
        jobs_api = JobsApi(api_client)
        
        # Intenta listar los jobs (esto debería funcionar incluso si no hay jobs)
        jobs = jobs_api.list_jobs()
        print("Conexión exitosa a Databricks!")
        print(f"Número de jobs encontrados: {len(jobs)}")
    except Exception as e:
        print(f"Error al conectar a Databricks: {e}")

if __name__ == "__main__":
    test_databricks_connection()
