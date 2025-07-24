import google.generativeai as genai
from dotenv import load_dotenv
import os
PDF_DOWNLOAD_FOLDER = "result"
load_dotenv()

MODEL_NAME = 'gemini-2.5-flash'
GOOGLE_API_KEY = "AIzaSyBWPhYzFFo1gRFjyUA4Vh1uskOLi-55hfU"
model = None
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(e)
