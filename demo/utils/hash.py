import re, hashlib

def cleanHashText(text):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    return hashlib.sha256(cleaned.encode('utf-8')).hexdigest()