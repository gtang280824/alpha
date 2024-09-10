import base64
import json
import requests

# Anaplan credentials
ANAPLAN_USER = "your_email"  # Your Anaplan username
ANAPLAN_PASSWORD = "your_password"  # Your Anaplan password
WORKSPACE_ID = "your_workspace_id"
MODEL_ID = "your_model_id"
FILE_ID = "your_file_id"  # File ID where CSV will be uploaded
IMPORT_ID = "your_import_id"  # Import Action ID to run after file upload

# Path to the CSV file
csv_file_path = 'rba_fx_rates_summary.csv'

# Base64 encode credentials
credentials = base64.b64encode(f"{ANAPLAN_USER}:{ANAPLAN_PASSWORD}".encode('utf-8')).decode('utf-8')


# Authenticate and get an authorization token
def get_auth_token():
    url = "https://auth.anaplan.com/token/authenticate"
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        auth_token = response.json().get('tokenValue')
        return auth_token
    else:
        print(f"Authentication failed: {response.text}")
        return None


# Upload CSV file to Anaplan
def upload_file(auth_token):
    url = f"https://api.anaplan.com/2/0/workspaces/{WORKSPACE_ID}/models/{MODEL_ID}/files/{FILE_ID}/chunks"
    headers = {
        'Authorization': f'AnaplanAuthToken {auth_token}',
        'Content-Type': 'application/octet-stream'
    }

    with open(csv_file_path, 'rb') as f:
        file_data = f.read()

    response = requests.put(url, headers=headers, data=file_data)

    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print(f"File upload failed: {response.text}")


# Run import action to load the CSV into Anaplan
def run_import(auth_token):
    url = f"https://api.anaplan.com/2/0/workspaces/{WORKSPACE_ID}/models/{MODEL_ID}/imports/{IMPORT_ID}/tasks"
    headers = {
        'Authorization': f'AnaplanAuthToken {auth_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "localeName": "en_US"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Import action triggered successfully.")
        task_id = response.json().get("task", {}).get("taskId")
        return task_id
    else:
        print(f"Failed to trigger import action: {response.text}")
        return None


# Monitor import status
def monitor_import_status(auth_token, task_id):
    url = f"https://api.anaplan.com/2/0/workspaces/{WORKSPACE_ID}/models/{MODEL_ID}/imports/{IMPORT_ID}/tasks/{task_id}"
    headers = {
        'Authorization': f'AnaplanAuthToken {auth_token}',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        task_status = response.json().get("task", {}).get("taskState")
        print(f"Task Status: {task_status}")
        return task_status
    else:
        print(f"Failed to get import status: {response.text}")
        return None


# Main process to authenticate, upload file, run import, and check status
def upload_and_import():
    # Get authentication token
    auth_token = get_auth_token()
    if not auth_token:
        return

    # Upload CSV file to Anaplan
    upload_file(auth_token)

    # Run the import action
    task_id = run_import(auth_token)
    if not task_id:
        return

    # Monitor the import process
    import_status = monitor_import_status(auth_token, task_id)
    while import_status not in ['COMPLETE', 'FAILED']:
        print("Waiting for import to complete...")
        import_status = monitor_import_status(auth_token, task_id)

    if import_status == "COMPLETE":
        print("Data imported successfully!")
    else:
        print("Data import failed.")


# Call the main function
upload_and_import()
