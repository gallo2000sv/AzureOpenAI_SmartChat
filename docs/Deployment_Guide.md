# Deployment Configuration Guide

## Streamlit Service Setup

1. Create the service file:
```bash
sudo nano /etc/systemd/system/streamlit.service
```

2. Copy the content from `examples/streamlit.service` and replace:
   - `your_username` with your system username
   - `your_project_path` with the path to your project
   - `your_venv_name` with your virtual environment name
   - Databricks configuration with your actual values

3. Set proper permissions:
```bash
sudo chmod 644 /etc/systemd/system/streamlit.service
```

4. Enable and start the service:
```bash
sudo systemctl enable streamlit
sudo systemctl start streamlit
```

5. Check service status:
```bash
sudo systemctl status streamlit
```

## Nginx Configuration

1. Create the Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/your_domain
```

2. Copy the content from `examples/nginx.conf` and replace:
   - `your_domain.com` with your actual domain
   - `your_username` with your system username
   - Adjust SSL certificate paths if needed

3. Create symbolic link:
```bash
sudo ln -s /etc/nginx/sites-available/your_domain /etc/nginx/sites-enabled/
```

4. Test Nginx configuration:
```bash
sudo nginx -t
```

5. If test is successful, restart Nginx:
```bash
sudo systemctl restart nginx
```

## Important Notes

1. SSL Certificates:
   - The configuration assumes you're using Let's Encrypt
   - Adjust paths if using different SSL provider

2. Permissions:
   - Ensure proper file permissions
   - Nginx user needs access to project directory

3. Ports:
   - Streamlit runs on port 8501
   - FastAPI runs on port 8000
   - Ensure these ports are available and firewalls configured

4. Environment Variables:
   - Keep Databricks tokens secure
   - Consider using `.env` file for local development

## Troubleshooting

1. Check service logs:
```bash
sudo journalctl -u streamlit
```

2. Check Nginx logs:
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

3. Common issues:
   - Permission denied: Check file and directory permissions
   - Connection refused: Ensure services are running
   - SSL errors: Verify certificate paths and renewal
