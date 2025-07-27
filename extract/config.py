import os
from dotenv import load_dotenv
load_dotenv()
MODEL_NAME = 'gemini-1.5-flash-latest'
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')
PDF_DOWNLOAD_FOLDER = 'downloaded_pdfs'
OUTPUT_FILENAME_JSON = 'hasil_ekstraksi_putusan.json'


