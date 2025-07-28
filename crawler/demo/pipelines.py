# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from itemadapter import ItemAdapter
from demo.utils.hash import cleanHashText
from datetime import datetime
from demo.utils.convertDate import convert_to_ymd
from demo.utils.etl.db import readData,insertPutusan
import json

class FormattingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        desc = adapter["description"]
        adapter["link_detail"] = adapter["url"]
        adapter["hash_id"] = cleanHashText(desc.get("nomor") or adapter["nomor"])
        adapter["scraped_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if "catatan_amar" in desc and desc["catatan_amar"]:
            desc["catatan_amar"] = re.sub(r'\s[^a-zA-Z0-9\s-]\s', ' ', desc["catatan_amar"]).lower()
        
        if "tanggal_register" in desc and desc["tanggal_register"]:
            desc["tanggal_register"] = convert_to_ymd(desc["tanggal_register"])
        
        if "tanggal_dibacakan" in desc and desc["tanggal_dibacakan"]:
            desc["tanggal_dibacakan"] = convert_to_ymd(desc["tanggal_dibacakan"])
        
        if "tanggal_musyawarah" in desc and desc["tanggal_musyawarah"]:
            desc["tanggal_musyawarah"] = convert_to_ymd(desc["tanggal_musyawarah"])
        
        if "hakim_ketua" in desc and desc["hakim_ketua"]:
            desc["hakim_ketua"] = desc["hakim_ketua"].replace("Hakim Ketua","")
        
        if "hakim_anggota" in desc and desc["hakim_anggota"]:
            desc["hakim_anggota"] = json.dumps(desc["hakim_anggota"].strip().replace("Hakim Anggota","").split(","))
        
        if "panitera" in desc and desc["panitera"]:
            desc["panitera"] = re.sub(r'Panitera Pengganti\s*:?', '', desc["panitera"])
        
        if "kaidah" in desc and desc["kaidah"]:
            desc["kaidah"] = re.sub(r'—', '', desc["kaidah"])
        insertPutusan(adapter)
        return dict(adapter)
    
    