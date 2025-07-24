import google.generativeai as genai
import json
import os
import json
import pandas as pd
import fitz  # PyMuPDF
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv


PROMPT_UNIVERSAL = """
Anda adalah asisten hukum AI yang sangat ahli dalam menganalisis dan menstrukturkan dokumen putusan pengadilan di Indonesia.
Tugas Anda adalah membaca teks putusan berikut dan mengekstrak semua informasi yang relevan ke dalam format JSON yang telah ditentukan di bawah ini.
STRUKTUR JSON YANG WAJIB DIIKUTI:
{{
  "klasifikasi_perkara": "string (Pilih dari: Pidana Umum, Pidana Khusus, Pidana Militer, Perdata, Perdata Agama, Perdata Khusus, TUN, Pajak)",
  "informasi_umum": {{
    "nomor_putusan": "string",
    "nama_pengadilan": "string",
    "tingkat_pengadilan": "string (Contoh: Pengadilan Negeri, Pengadilan Tinggi, Mahkamah Agung)",
    "tanggal_putusan": "string (format: YYYY-MM-DD)"
  }},
  "para_pihak": [
    {{
      "peran_pihak": "string (Contoh: Terdakwa, Penggugat, Pemohon)",
      "nama_lengkap": "string",
      "tempat_lahir": "string",
      "tanggal_lahir": "string (format: YYYY-MM-DD)",
      "usia": "integer",
      "jenis_kelamin": "string",
      "pekerjaan": "string",
      "agama": "string",
      "alamat": "string",
      "nomor_ktp": "string",
      "nomor_kk": "string",
      "nomor_akta_kelahiran": "string",
      "nomor_paspor": "string"
    }}
  ]
}}
INSTRUKSI PENTING:
1.`para_pihak`: Selalu dalam format LIST. Ekstrak SEMUA pihak yang terlibat.
2.`RANGKUMAN`: Untuk semua field deskriptif, buatlah rangkuman inti sarinya saja.
3.`NOMOR IDENTITAS`: Untuk `nomor_ktp`, dll., ekstrak HANYA ANGKA-nya saja.
4.`null`: Jika informasi tidak ditemukan, WAJIB gunakan nilai null.
Sekarang, analisis teks putusan berikut dan buatlah JSON yang sesuai.
Teks Putusan: {teks_pdf}
"""

def ekstrak_data_dengan_gemini(model, teks_pdf):
    if not model:
        print("Undefined Model")
        return None        
    try:
        prompt = PROMPT_UNIVERSAL.format(teks_pdf=teks_pdf)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        with open("result.json",'w') as file:
          file.write(json.dumps(json.loads(response.text)))
          # return json.loads(response.text)
    except Exception as e:
        print(e)
        return None