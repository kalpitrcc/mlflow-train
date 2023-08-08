import os
import requests
from minio import Minio

# Minio configuration
minio_url = "your-minio-url"
minio_access_key = "your-minio-access-key"
minio_secret_key = "your-minio-secret-key"
bucket_name = "your-bucket-name"
model_artifact_path = "path/to/your/model"

# JFrog Artifactory configuration
artifactory_url = "https://your-artifactory-url"
artifactory_repo = "your-repo"
api_key = "your-api-key"

# Initialize Minio client
minio_client = Minio(minio_url, access_key=minio_access_key, secret_key=minio_secret_key, secure=False)

# Download model files from Minio
download_dir = "downloaded_model"
os.makedirs(download_dir, exist_ok=True)

for obj in minio_client.list_objects(bucket_name, prefix=model_artifact_path, recursive=True):
    file_name = os.path.basename(obj.object_name)
    file_path = os.path.join(download_dir, file_name)
    minio_client.fget_object(bucket_name, obj.object_name, file_path)

# Upload downloaded model files to JFrog Artifactory
upload_url = f"{artifactory_url}/{artifactory_repo}/{model_artifact_path}"
headers = {
    "X-JFrog-Art-Api": api_key,
}

for file_name in os.listdir(download_dir):
    file_path = os.path.join(download_dir, file_name)
    with open(file_path, 'rb') as model_file:
        response = requests.put(f"{upload_url}/{file_name}", data=model_file, headers=headers)

        if response.status_code == 201:
            print(f"File {file_name} uploaded successfully.")
        else:
            print(f"Failed to upload file {file_name}. Response:", response.text)


'''


headers = {
    "Authorization": "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode(),
}

'''
