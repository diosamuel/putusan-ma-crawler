import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
PROMPT_UNIVERSAL = """
Anda adalah asisten hukum AI yang sangat ahli dalam menganalisis dan menstrukturkan dokumen putusan pengadilan di Indonesia.
Tugas Anda adalah membaca teks putusan berikut dan mengekstrak semua informasi yang relevan ke dalam format JSON yang telah ditentukan di bawah ini.
STRUKTUR JSON YANG WAJIB DIIKUTI:
{{
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
      "NIK/nomor NIK": "string",
      "nomor_kk": "string",
      "nomor_akta_kelahiran": "string",
      "nomor_paspor": "string"
    }}
  ]
}}
Sekarang, analisis teks putusan berikut dan buatlah JSON yang sesuai.
---
Teks Putusan: {teks_pdf}
---
"""
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv('GEMINI_MODEL')
def extract(text):
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    headers = { "Content-Type": "application/json" }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": text}
                ]
            }
        ]
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        text = result['candidates'][0]['content']['parts'][0]['text']
        return text