mport os
import requests

# JFrog Artifactory parameters
artifactory_url = 'https://your-artifactory-instance.jfrog.io/artifactory'
repository = 'your-repo'
username = 'your-username'
password = 'your-password'

# Local file path and target path in Artifactory
local_file_path = 'path/to/local/file.txt'
target_artifact_path = 'path/in/artifactory/file.txt'

# Construct the upload URL
upload_url = f'{artifactory_url}/{repository}/{target_artifact_path}'

# Read the file content
with open(local_file_path, 'rb') as file:
    file_content = file.read()

# Set headers for authentication
headers = {'Authorization': f'Basic {username}:{password}'}

# Perform the file upload
response = requests.put(upload_url, data=file_content, headers=headers)

if response.status_code == 201:
    print(f'File uploaded successfully to {upload_url}')
else:
    print(f'Failed to upload file. Status code: {response.status_code}')
    print(response.text)
