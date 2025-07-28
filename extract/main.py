import os
import json
import time
import google.generativeai as genai
import boto3
from botocore.client import Config
import extract.config as config
from extract.url_process import putusanProcess 
from crawler.demo.utils.etl.db import insertData
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from crawler.demo.utils.etl.db import readData
import logging
def setup():
    if config.GOOGLE_API_KEY:
        try:
            genai.configure(api_key=config.GOOGLE_API_KEY)
            model = genai.GenerativeModel(config.MODEL_NAME)
            return model
        except Exception as e:
            logging.error(f"Konfigurasi API gagal: {e}")
            return None
    else:
        logging.error("Kunci API tidak tersedia di config.py atau .env file.")
        return None

def setupS3():
    """Mengkonfigurasi dan mengembalikan S3 client untuk MinIO."""
    print("Menyiapkan koneksi ke MinIO...")
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=f'http://{config.MINIO_ENDPOINT}',
            aws_access_key_id=config.MINIO_ACCESS_KEY,
            aws_secret_access_key=config.MINIO_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        print("Koneksi MinIO berhasil.")
        return s3_client
    except Exception as e:
        print(f"Koneksi MinIO gagal: {e}")
        return None

def main(list_url_putusan):
    model = setup()
    s3_client = setupS3()
    
    if not model or not s3_client:
        logging.error("Eksekusi dihentikan karena konfigurasi gagal.")
        return
    
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
                logging.error("Gagal memproses URL ini.\n")
            if i < len(urls_to_process) - 1:
                time.sleep(5)

    if list_hasil_akhir:
        logging.info(f"\nMenyimpan total {len(list_hasil_akhir)} data ke dalam file JSON...")
        logging.info(list_hasil_akhir)
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
        logging.info("Tidak ada data yang berhasil diekstrak.")

result = readData('link_detail','informasi_putusan')
list_putusan = list(map(lambda x:x[0],result.result_rows))
main(list_putusan)