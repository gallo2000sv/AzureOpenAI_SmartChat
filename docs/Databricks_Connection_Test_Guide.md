# Databricks Connection Test Guide

## Overview
The `test_databricks_connection.py` script helps verify your Databricks connection settings.

## Location
Save this script in `app/backend/test_databricks_connection.py`:

```python
import os
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.jobs.api import JobsApi

DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

print(f"DATABRICKS_HOST: {DATABRICKS_HOST}")
print(f"DATABRICKS_TOKEN: {'*' * len(DATABRICKS_TOKEN) if DATABRICKS_TOKEN else 'Not set'}")

def test_databricks_connection():
    try:
        api_client = ApiClient(host=DATABRICKS_HOST, token=DATABRICKS_TOKEN)
        jobs_api = JobsApi(api_client)
        
        # Try to list jobs (this should work even if there are no jobs)
        jobs = jobs_api.list_jobs()
        print("Successfully connected to Databricks!")
        print(f"Number of jobs found: {len(jobs)}")
    except Exception as e:
        print(f"Error connecting to Databricks: {e}")

if __name__ == "__main__":
    test_databricks_connection()
```

## Usage
1. Ensure your virtual environment is activated
2. Set your environment variables:
   ```bash
   export DATABRICKS_HOST="your-host"
   export DATABRICKS_TOKEN="your-token"
   ```
3. Run the test:
   ```bash
   python test_databricks_connection.py
   ```

## Troubleshooting
- If host is not found: Verify DATABRICKS_HOST
- If authentication fails: Check DATABRICKS_TOKEN
- If permission denied: Verify token permissions
