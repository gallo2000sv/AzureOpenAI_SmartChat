# Databricks and Azure Storage Configuration Guide

## Azure Storage Setup (Required First)
### 1. Create Azure Storage Account
1. Go to Azure Portal (https://portal.azure.com)
2. Navigate to "Storage accounts"
3. Click "+ Create"
4. Fill in the required information:
   - Subscription: Choose your subscription
   - Resource group: Create new or select existing
   - Storage account name: Enter a unique name
   - Region: Choose your preferred region
   - Performance: Standard
   - Redundancy: Locally redundant storage (LRS)
5. Click "Review + Create"
6. Once created, note down:
   - Storage account name
   - Access key (found in "Access keys" section)

### 2. Create Container
1. Go to your new storage account
2. Navigate to "Containers"
3. Click "+ Container"
4. Enter a name for your container
5. Set "Public access level" to "Private"
6. Click "Create"

## Databricks Secrets Scopes Configuration Guide
### Prerequisites for Windows/Linux
1. Install Python 3.6 or higher 
2. Install Databricks CLI: `pip install databricks-cli`
3. Access to Azure Databricks workspace

### Initial Setup
#### 1. Generate Access Token
1. Go to your Databricks workspace
2. Click on your profile icon (top right corner)
3. Select "Settings"
4. Select "Developer"
5. On Access tokens section click on "Manage" button
6. Click "Generate New Token"
7. Enter a description and expiration
8. Copy the generated token

#### 2. Configure Databricks CLI
```bash
databricks configure --token
```
Enter:
- Databricks Host URL (e.g., https://your-workspace.azuredatabricks.net)
- Your access token you just got on previous step (Initial Setup)

### Create New Secret Scope
```bash
# Create scope
databricks secrets create-scope --scope your_storage_scope --initial-manage-principal users

# Add secret
databricks secrets put --scope your_storage_scope --key your_storage_access_key
```
When prompted, enter your Azure Storage access key from the first section.

### Managing Secret Scopes
#### Check Existing Scopes
```bash
# List all secret scopes
databricks secrets list-scopes

# List secrets in a specific scope
databricks secrets list --scope your_storage_scope
```

### Using Secrets in Notebook
```python
# Access secret in this notebook
secret_value = dbutils.secrets.get(scope="your_storage_scope", key="your_storage_access_key")
```

## Required Secrets for This Project
1. Azure Storage Access:
   - Scope: `your_storage_scope`
   - Key: `your_storage_access_key`

These values should match what you used in the "Create New Secret Scope" step above.

## Connecting to Azure Storage in Notebook
After setting up your secret scope, we will use this code in our notebook to connect to Azure Storage (it's already included in /examples/databricks_notebook.py):
```python
storage_account_name = "your_storage_account_name"
container_name = "your_container_name"
access_key = dbutils.secrets.get(scope="your_storage_scope", key="your_storage_access_key")

# Configure Spark to connect to Azure Storage
spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net",
    access_key
)
```

## Troubleshooting
- If you get permission errors, ensure your user has the correct access level
- If secrets aren't visible, verify the scope name is correct
- For access issues, regenerate your access token and reconfigure CLI
- If storage connection fails, verify your Azure Storage account name and access key
- Ensure your IP address is allowed in Azure Storage network settings

## Next Steps
After completing this setup:
1. Your Azure Storage account is ready
2. Your container is created
3. Your Databricks secrets are configured
4. You can securely access your storage from Databricks notebooks

You can now proceed to upload your data to the container and access it from your Databricks notebooks.
