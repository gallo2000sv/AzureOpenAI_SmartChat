# AI-Powered Data Analysis Chatbot: Azure, Databricks, and OpenAI Integration

## Overview
This project implements an email analysis system powered by Azure Databricks, FastAPI, and Streamlit. It processes and analyzes email data stored in a CSV file (or any other type if you specify it in the notebook code) in Azure Blob Storage and provides insights through an interactive web interface.

## Project Structure
```
📁 project-root/
├── 📁 docs/
│   ├── Accessing_the_app_guide.md    # Application access instructions
│   ├── DATABRICKS_SETUP.md           # Databricks and Azure Storage configuration
│   ├── Databricks_Connection_Test_Guide.md  # Connection testing guide
│   ├── Deployment_Guide.md           # Production deployment instructions
│   └── Nginx_Config.md               # Nginx server configuration
├── 📁 examples/
│   ├── nginx.conf                    # Example Nginx configuration
│   └── streamlit.service            # Example Streamlit service configuration
├── 📁 notebooks/
│   └── .env                         # Environment variables for notebooks
├── main.py                         # FastAPI backend
├── streamlit_app.py               # Streamlit frontend
├── test_databrickconnection.py    # Databricks connection test script
├── requirements.txt               # Project dependencies
├── .gitignore
├── LICENSE
└── README.md
```

## Prerequisites
- Python 3.8+
- Azure Databricks workspace
- Azure Storage account with Blob container
- Nginx server (for production deployment)

## Local Development Setup

1. Create and activate virtual environment:
```bash
# Windows
python -m venv chatbot_env
chatbot_env\Scripts\activate

# Linux/Mac
python3 -m venv chatbot_env
source chatbot_env/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Databricks connection:
- Follow [DATABRICKS_SETUP.md](docs/DATABRICKS_SETUP.md) for detailed instructions
- Test your connection using the test script:
  ```bash
  python test_databrickconnection.py
  ```

4. Start the applications:
```bash
# Start FastAPI backend
uvicorn main:app --reload --port 8000

# In a new terminal, start Streamlit frontend
streamlit run streamlit_app.py
```

## Documentation
- [Application Access Guide](docs/Accessing_the_app_guide.md) - How to access and use the application
- [Databricks Setup](docs/DATABRICKS_SETUP.md) - Azure Storage and Databricks configuration
- [Databricks Connection Test](docs/Databricks_Connection_Test_Guide.md) - How to test your Databricks connection
- [Deployment Guide](docs/Deployment_Guide.md) - Production deployment steps
- [Nginx Config](docs/Nginx_Config.md) - Web server configuration

## Application Access

### Development URLs
- Streamlit Interface: `http://localhost:8501`
- FastAPI Backend: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

### Production URLs
- Main Application: `https://your_domain.com/your_app_path/`
- API Endpoint: `https://your_domain.com/api/`
- API Documentation: `https://your_domain.com/api/docs`

For detailed access instructions, see [Accessing_the_app_guide.md](docs/Accessing_the_app_guide.md)

## Configuration Files

### Nginx Configuration
See [examples/nginx.conf](examples/nginx.conf) for the recommended server configuration.

### Systemd Service
See [examples/streamlit.service](examples/streamlit.service) for the Streamlit service configuration.

## Troubleshooting

### Common Issues
1. Databricks Connection:
   - Verify environment variables are set correctly
   - Ensure Databricks token has not expired
   - Run `test_databrickconnection.py` to verify connection

2. Application Access:
   - For local development, ensure ports 8000 and 8501 are available
   - For production, check Nginx logs if URLs are not accessible
   - Verify SSL certificates are properly configured

3. Virtual Environment:
   - Ensure virtual environment is activated
   - Verify all dependencies are installed
   - Check Python version compatibility

### Logging
- FastAPI logs: Check your terminal running the FastAPI server
- Streamlit logs: Check your terminal running the Streamlit application
- Production logs: 
  ```bash
  sudo journalctl -u streamlit
  sudo tail -f /var/log/nginx/error.log
  ```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
