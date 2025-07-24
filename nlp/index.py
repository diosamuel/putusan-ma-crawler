import fitz  
import requests
from bs4 import BeautifulSoup
import os
from gemini import ekstrak_data_dengan_gemini
import config

def extractURL(url):
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
            page_response = requests.get(url, headers=headers, timeout=15)
            page_response.raise_for_status()
            
            soup = BeautifulSoup(page_response.content, 'html.parser')
            pdf_link_tag = soup.find('a', href=lambda href: href and "/pdf/" in href)
            
            if not pdf_link_tag:
                print("  └─ ✗ Link unduhan PDF tidak ditemukan.")
                return None
                
            pdf_url = pdf_link_tag['href']
            print(f"  └─ ✓ Link PDF ditemukan: {pdf_url}")

        pdf_response = requests.get(pdf_url, headers=headers, timeout=30)
        pdf_response.raise_for_status()
        pdf_content = pdf_response.content
        
        pdf_filename = pdf_url.split('/')[-1]
        if not pdf_filename.lower().endswith('.pdf'):
            pdf_filename += ".pdf"
            
        # Menggunakan variabel PDF_DOWNLOAD_FOLDER dari config.py
        save_path = os.path.join(config.PDF_DOWNLOAD_FOLDER, pdf_filename)
        with open(save_path, 'wb') as f:
            f.write(pdf_content)
        print(f"  └─ ✓ PDF berhasil diunduh dan disimpan di: {save_path}")
        
        with fitz.open(stream=pdf_content, filetype="pdf") as doc:
            full_text = "".join(page.get_text() for page in doc)
        
        if not full_text.strip():
            print("  └─ ✗ Gagal mengekstrak teks dari PDF.")
            return None
            
        print("  └─ Mengirim teks ke Gemini untuk ekstraksi...")
        # PERBAIKAN: Meneruskan 'model' ke fungsi ekstraksi
        hasil_json = ekstrak_data_dengan_gemini(model, full_text)
        
        if hasil_json:
            hasil_json['sumber_url'] = url
            hasil_json['nama_file_lokal'] = pdf_filename
        
        return hasil_json

    except Exception as e:
        print(f"  └─ ✗ Terjadi error: {e}")
        return None
