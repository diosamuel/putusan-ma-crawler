import boto3
from botocore.client import Config
import os
from dotenv import load_dotenv
load_dotenv()
s3_client = boto3.client(
    's3',
    endpoint_url=f'http://{os.getenv("MINIO_HOST","localhost")}:{os.getenv("MINIO_API_PORT","9000")}',
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY","default"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY","default"),
    config=Config(signature_version='s3v4')
)


response = s3_client.list_buckets()
# buckets = response.get('Buckets', [])

print(response)