import fitz
import requests
from bs4 import BeautifulSoup
import io
import os
from extract.extractor import geminiExtract
import extract.config as config

def putusanProcess(model, s3_client, url):
    print(f"Memproses URL: {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        pdf_content = None
        pdf_filename = ""

        if url.lower().endswith('.pdf'):
            print("  └─ Terdeteksi link PDF langsung. Mengunduh file...")
            pdf_url = url
        else:
            print("  └─ Terdeteksi link halaman web. Mencari link PDF...")
            page_response = requests.get(url, headers=headers, timeout=25)
            page_response.raise_for_status()
            
            soup = BeautifulSoup(page_response.content, 'html.parser')
            pdf_link_tag = soup.find('a', href=lambda href: href and "/pdf/" in href)
            
            if not pdf_link_tag:
                print("  └─ ✗ Link unduhan PDF tidak ditemukan.")
                return None
                
            pdf_url = pdf_link_tag['href']
            print(f"  └─ ✓ Link PDF ditemukan: {pdf_url}")

        # Unduh konten file PDF
        pdf_response = requests.get(pdf_url, headers=headers, timeout=30)
        pdf_response.raise_for_status()
        pdf_content = pdf_response.content
        print("  └─ ✓ Konten PDF berhasil diunduh ke memori.")
        
        # Membuat nama file dari bagian akhir URL
        pdf_filename = pdf_url.split('/')[-1]
        if not pdf_filename.lower().endswith('.pdf'):
            pdf_filename += ".pdf"
        
        # PERUBAHAN: Mengganti penyimpanan lokal dengan unggahan ke MinIO
        print(f"  └─ Mengunggah '{pdf_filename}' ke bucket MinIO '{config.MINIO_BUCKET_NAME}'...")
        s3_client.put_object(
            Bucket=config.MINIO_BUCKET_NAME,
            Key=pdf_filename,
            Body=pdf_content,
            ContentLength=len(pdf_content),
            ContentType='application/pdf'
        )
        print("  └─ ✓ PDF berhasil diunggah ke MinIO.")
        
        # Ekstrak teks dari konten PDF di memori
        with fitz.open(stream=io.BytesIO(pdf_content), filetype="pdf") as doc:
            full_text = "".join(page.get_text() for page in doc)
        
        if not full_text.strip():
            print("  └─ ✗ Gagal mengekstrak teks dari PDF.")
            return None
            
        print("  └─ Mengirim teks ke Gemini untuk ekstraksi...")
        hasil_json = geminiExtract(model, full_text)
        
        if hasil_json:
            hasil_json['sumber_url'] = url
            hasil_json['nama_file_minio'] = pdf_filename # Mengganti nama field agar lebih jelas
        
        return hasil_json

    except Exception as e:
        print(f"  └─ ✗ Terjadi error: {e}")
        return None
