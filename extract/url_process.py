import fitz
import requests
import io
import logging
import os
from bs4 import BeautifulSoup
from extract.extractor import geminiExtract
from dotenv import load_dotenv
load_dotenv()
def putusanProcess(model, s3_client, url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        pdf_content = None
        pdf_filename = ""
        if url.lower().endswith('.pdf'):
            pdf_url = url
        else:
            page_response = requests.get(url, headers=headers, timeout=25)
            page_response.raise_for_status()
            soup = BeautifulSoup(page_response.content, 'html.parser')
            pdf_link_tag = soup.find('a', href=lambda href: href and "/pdf/" in href)
            if not pdf_link_tag:
                logging.error("Link unduhan PDF tidak ditemukan.")
                return None      
            pdf_url = pdf_link_tag['href']

        pdf_response = requests.get(pdf_url, headers=headers, timeout=30)
        pdf_response.raise_for_status()
        pdf_content = pdf_response.content
        pdf_filename = pdf_url.split('/')[-1]
        if not pdf_filename.lower().endswith('.pdf'):
            pdf_filename += ".pdf"
        
        logging.info(f"Mengunggah '{pdf_filename}' ke bucket MinIO '{config.MINIO_BUCKET_NAME}'...")
        s3_client.put_object(
            Bucket=os.getenv("MINIO_BUCKET_NAME"),
            Key=pdf_filename,
            Body=pdf_content,
            ContentLength=len(pdf_content),
            ContentType='application/pdf'
        )
    
        with fitz.open(stream=io.BytesIO(pdf_content), filetype="pdf") as doc:
            full_text = "".join(page.get_text() for page in doc)
        
        if not full_text.strip():
            return None
        
        hasil_json = geminiExtract(model, full_text)    
        if hasil_json:
            hasil_json['sumber_url'] = url
            hasil_json['nama_file_minio'] = pdf_filename
        
        return hasil_json

    except Exception as e:
        logging.error(e)
        return None
