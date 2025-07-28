import os
import json
import time
import google.generativeai as genai
import sys
import logging
import boto3
from botocore.client import Config
from datetime import datetime
from extract.url_process import putusanProcess 
from crawler.demo.utils.etl.db import insertData
from crawler.demo.utils.etl.db import readData
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def setupGeminiModel():
    if os.getenv("GEMINI_API_KEY"):
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel(os.getenv("MODEL_NAME"))
            return model
        except Exception as e:
            logging.error(f"Wrong API config {e}")
            return None
    else:
        logging.error("Failed to retrieve gemini api key")
        return None

def setupS3MinIO():
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=f'http://{os.getenv("MINIO_HOST","localhost"):{os.getenv("MINIO_API_PORT","9000")}}',
            aws_access_key_id=os.getenv("MINIO_ACCESS_KEY","default"),
            aws_secret_access_key=os.getenv("MINIO_SECRET_KEY","default"),
            config=Config(signature_version='s3v4')
        )
        logging.info("MinIO Connect Success")
        return s3_client
    except Exception as e:
        logging.error(f"Failed MinIO connect {e}")
        return None

def main(list_url_putusan):
    model = setupGeminiModel()
    s3_client = setupS3MinIO()
    
    list_hasil_akhir = []
    if os.path.exists(config.OUTPUT_FILENAME_JSON):
        try:
            with open(config.OUTPUT_FILENAME_JSON, 'r', encoding='utf-8') as f:
                list_hasil_akhir = json.load(f)
        except json.JSONDecodeError:
            pass
    
    processed_urls = {item.get('sumber_url') for item in list_hasil_akhir}
    urls_to_process = [url for url in list_url_putusan if url not in processed_urls]

    if urls_to_process:
        for i, url in enumerate(urls_to_process):
            hasil = putusanProcess(model, s3_client, url)
            if hasil:
                list_hasil_akhir.append(hasil)
            else:
                logging.error(f"Error: {hasil}")
            if i < len(urls_to_process) - 1:
                time.sleep(5)

    if list_hasil_akhir:
        ekstraksi_columns = [
            'hash_id', 'peran_pihak', 'tempat_lahir', 'tanggal_lahir', 
            'usia', 'jenis_kelamin', 'pekerjaan', 'agama', 
            'nomor_ktp', 'nomor_kk', 'nomor_akta_kelahiran', 'nomor_paspor'
        ]
        
        for hasil in list_hasil_akhir:
            if 'para_pihak' in hasil and hasil['para_pihak']:
                for pihak in hasil['para_pihak']:
                    data = {
                        'hash_id': hasil.get('hash_id', ''),
                        'peran_pihak': pihak.get('peran_pihak', ''),
                        'tempat_lahir': pihak.get('tempat_lahir', ''),
                        'tanggal_lahir': pihak.get('tanggal_lahir', ''),
                        'usia': str(pihak.get('usia', '')),
                        'jenis_kelamin': pihak.get('jenis_kelamin', ''),
                        'pekerjaan': pihak.get('pekerjaan', ''),
                        'agama': pihak.get('agama', ''),
                        'nomor_ktp': str(pihak.get('nomor_ktp', '')) if pihak.get('nomor_ktp') else '',
                        'nomor_kk': str(pihak.get('nomor_kk', '')) if pihak.get('nomor_kk') else '',
                        'nomor_akta_kelahiran': str(pihak.get('nomor_akta_kelahiran', '')) if pihak.get('nomor_akta_kelahiran') else '',
                        'nomor_paspor': str(pihak.get('nomor_paspor', '')) if pihak.get('nomor_paspor') else '',
                        'upload': datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    insertData(data, 'ekstraksi_pdf', ekstraksi_columns)
    else:
        logging.warning("No Link to Extract")


result = readData('link_detail','informasi_putusan')
list_putusan = list(map(lambda x:x[0],result.result_rows))
main(list_putusan)