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
        print(f"== Process {url} == ")
        pdf_response = requests.get(
            url='https://proxy.scrapeops.io/v1/',
            params={
                'api_key': 'e2515043-1a68-4771-9aff-2a466faaf9af',
                'url': url, 
            },timeout=100)
        pdf_response.raise_for_status()
        pdf_content = pdf_response.content
        pdf_filename = url.split('/')[-1]
        if not pdf_filename.lower().endswith('.pdf'):
            pdf_filename += ".pdf"
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
