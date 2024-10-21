# AzureOpenAI_SmartChat
AI chatbot ingests diverse data (emails, chats) via Azure, processes it through Databricks, and uses OpenAI's API for analysis. Users query data in natural language through Streamlit UI. FastAPI backend manages requests securely. Delivers AI-driven insights from unstructured data, deployed on Ubuntu with robust security measures.
# Email Analysis Project

## Overview
This project implements an email analysis system using Azure Databricks, FastAPI, and Streamlit. It processes email data and provides insights through an interactive web interface.

## Project Structure
```
📁 app/           - Main application code
📁 docs/          - Detailed documentation
📁 examples/      - Example configuration files and notebooks
```

## Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables (see `.env.example`)
4. Start the backend: `uvicorn app.backend.main:app --reload`
5. Start the frontend: `streamlit run app/frontend/streamlit_app.py`

## Detailed Documentation
- [Databricks Setup](docs/DATABRICKS_SETUP.md)
- [Nginx Configuration](docs/NGINX_CONFIG.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Environment Setup](docs/ENVIRONMENT_SETUP.md)

## Prerequisites
- Python 3.8+
- Azure Databricks account
- Azure Storage account
- Nginx server (for production deployment)
