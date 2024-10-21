# Nginx Configuration Guide

## Overview
This document explains how to configure Nginx for serving the FastAPI backend and Streamlit frontend.

## Configuration Steps

### 1. Installation
```bash
sudo apt update
sudo apt install nginx
```

### 2. Configuration
1. Copy the example configuration from `examples/nginx.conf`
2. Modify the following values:
   - server_name
   - SSL certificate paths
   - Root directory paths

### 3. File Locations
- Main configuration: `/etc/nginx/nginx.conf`
- Site configuration: `/etc/nginx/sites-available/your-site`
- Create symbolic link: `ln -s /etc/nginx/sites-available/your-site /etc/nginx/sites-enabled/`

### 4. Service Configuration
1. Copy the Streamlit service file from `examples/streamlit.service`
2. Place it in `/etc/systemd/system/streamlit.service`
3. Update paths and environment variables

## Example Configurations
See the `examples/` directory for template configuration files:
- `nginx.conf`: Nginx server configuration
- `streamlit.service`: Systemd service configuration
