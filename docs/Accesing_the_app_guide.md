# Accessing the Application

## Development Environment
When running locally, the application is accessible at:
- Streamlit Interface: `http://localhost:8501`
- FastAPI Backend: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

## Production Environment
In the production server, the application is deployed to a specific directory and accessed through:
- Main Application: `https://your_domain.com/path_to_your_app/`
- API Endpoint: `https://your_domain.com/api/`
- API Documentation: `https://your_domain.com/api/docs`

Note: The actual production URLs will depend on:
1. Your domain name
2. The directory where you deploy the application
3. The paths configured in your Nginx configuration

For example, if you deploy to a directory called `dataprocessor` in your server:
```bash
# Server directory structure
/home/your_username/public_html/
└── dataprocessor/         # Deployment directory
    ├── chatbot_env/      # Virtual environment
    └── app/              # Application files
```

Your Nginx configuration would map this to:
```nginx
location /dataprocessor/ {
    proxy_pass http://localhost:8501/;
    # ... other configuration
}
```

And users would access the application at:
`https://your_domain.com/dataprocessor/`

## Deployment Directory
The deployment directory path is configured in:
1. Nginx configuration file
2. Streamlit service file
3. Any systemd service files

Make sure these paths match your actual server setup.
