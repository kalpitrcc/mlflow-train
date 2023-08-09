import boto3
from botocore.client import Config
import zipfile
import os

# Configure the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

# Specify the S3 bucket and folder (prefix) to download from
bucket_name = 'your-bucket'
folder_prefix = 'path/to/folder/'

# List objects in the specified folder
objects = s3_client.list_objects(Bucket=bucket_name, Prefix=folder_prefix)['Contents']

# Determine the latest object (folder) based on last modified timestamp
latest_object = max(objects, key=lambda x: x['LastModified'])

# Create a temporary directory for downloading files
download_dir = './temp_download/'
os.makedirs(download_dir, exist_ok=True)

# Download objects from the latest folder and store them in the temporary directory
for obj in objects:
    object_key = obj['Key']
    local_filename = os.path.join(download_dir, os.path.basename(object_key))
    
    s3_client.download_file(bucket_name, object_key, local_filename)

# Create a zip file containing the downloaded objects
zip_filename = 'latest_folder.zip'
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for root, _, files in os.walk(download_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, download_dir)
            zipf.write(file_path, arcname)

# Clean up: Delete the temporary downloaded files
for obj in objects:
    object_key = obj['Key']
    local_filename = os.path.join(download_dir, os.path.basename(object_key))
    os.remove(local_filename)

os.rmdir(download_dir)

print(f'Latest folder downloaded and zipped as: {zip_filename}')
