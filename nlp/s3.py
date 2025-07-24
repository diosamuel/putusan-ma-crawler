import boto3
from botocore.client import Config

# MinIO connection details
endpoint_url = "http://localhost:9002"  # or wherever your MinIO server runs
access_key = "root"
secret_key = "mdmedia123"
bucket_name = "putusanma"
object_name = "result/zaf0683df093feda91b9313032363038.pdf"
pdf_file_path = "report.pdf"  # local path to PDF

# Connect to MinIO using boto3
s3 = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

# Make sure the bucket exists (create if not)
try:
    s3.head_bucket(Bucket=bucket_name)
except:
    s3.create_bucket(Bucket=bucket_name)

# Upload the PDF
with open(pdf_file_path, 'rb') as f:
    s3.upload_fileobj(f, bucket_name, object_name)

print("✅ PDF uploaded successfully to MinIO!")
