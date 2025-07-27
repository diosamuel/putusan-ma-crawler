import os
import json
import time
import google.generativeai as genai
import boto3
from botocore.client import Config
import extract.config as config
from extract.url_process import putusanProcess 
import sys
import os
# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# from crawler.demo.utils.etl.db import readData
import logging
def setup():
    """Mengkonfigurasi dan mengembalikan model Gemini menggunakan variabel dari config."""
    if config.GOOGLE_API_KEY:
        try:
            genai.configure(api_key=config.GOOGLE_API_KEY)
            model = genai.GenerativeModel(config.MODEL_NAME)
            print("Konfigurasi Gemini API berhasil.")
            return model
        except Exception as e:
            print(f"Konfigurasi API gagal: {e}")
            return None
    else:
        print("Kunci API tidak tersedia di config.py atau .env file.")
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
        print("Eksekusi dihentikan karena konfigurasi gagal.")
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

    if not urls_to_process:
        print("\nSemua URL sudah diproses sebelumnya.")
    else:
        print(f"\nMenemukan {len(urls_to_process)} URL baru untuk diproses.")
        for i, url in enumerate(urls_to_process):
            # Meneruskan objek 'model' dan 's3_client' ke dalam fungsi pemroses
            hasil = putusanProcess(model, s3_client, url)
            if hasil:
                list_hasil_akhir.append(hasil)
                print("  └─ Ekstraksi dari URL berhasil!\n")
            else:
                print("  └─ Gagal memproses URL ini.\n")
            
            # Jeda antar file untuk menghindari limit API
            if i < len(urls_to_process) - 1:
                time.sleep(5) # Menggunakan jeda 5 detik yang lebih cepat

    if list_hasil_akhir:
        print(f"\nMenyimpan total {len(list_hasil_akhir)} data ke dalam file JSON...")
        # Menggunakan nama file output dari config.py
        with open(config.OUTPUT_FILENAME_JSON, 'w', encoding='utf-8') as f:
            json.dump(list_hasil_akhir, f, ensure_ascii=False, indent=4)
        print(f"Data berhasil disimpan di '{config.OUTPUT_FILENAME_JSON}'")
    else:
        print("\nTidak ada data yang berhasil diekstrak.")

# res = readData('link_detail','informasi_putusan')
# print(res)

main(["https://putusan3.mahkamahagung.go.id/direktori/putusan/zaf06973aa83b0b6bd69323332333135.html"])
