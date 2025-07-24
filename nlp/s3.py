endpoint_url = "http://localhost:9002"  # or wherever your MinIO server runs
access_key = "root"
secret_key = "mdmedia123"
bucket_name = "putusanma"
object_name = "result/zaf0683df093feda91b9313032363038.pdf"
pdf_file_path = "report.pdf"  # local path to PDF

from minio import Minio
from dotenv import load_dotenv

import os
load_dotenv()
LOCAL_FILE_PATH = object_name
ACCESS_KEY = "root"
SECRET_KEY = "mdmedia123"
MINIO_API_HOST = "http://localhost:9001"
MINIO_CLIENT = Minio("localhost:9001", access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
def main():
    found = MINIO_CLIENT.bucket_exists("putusanma")
    if not found:
        MINIO_CLIENT.make_bucket("putusanma")
    else:
        print("Bucket already exists")
        MINIO_CLIENT.fput_object("putusanma", object_name,LOCAL_FILE_PATH,)
    print("It is successfully uploaded to bucket")
main()