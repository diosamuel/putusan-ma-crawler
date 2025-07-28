import google.generativeai as genai
import json
import logging
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

def geminiExtract(model, teks_pdf):
    """
    Menganalisis teks PDF menggunakan model Gemini yang diberikan dan prompt universal.
    """
    try:
        prompt = PROMPT_UNIVERSAL.format(teks_pdf=teks_pdf)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
      logging.info(e)
      return None
