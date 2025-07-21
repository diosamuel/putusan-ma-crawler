# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import re

from itemadapter import ItemAdapter
from demo.utils.hash import cleanHashText
from datetime import datetime

# import pendulum as pm

# class DuplicatePipeline:
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         if "hash_id" in adapter.keys():
#             adapter['hash_id'] = cleanHashText(adapter['nomor_putusan']+adapter["register"])
#             # for dateAdapter in ["register","putus","upload"]:
#                 # adapter[dateAdapter] = pm.from_format(adapter[dateAdapter],"DD-MM-YYYY").to_date_string()
#         return item

mapperDate = {
    "januari":"january",
    "februari":"february",
    "maret":"march",
    "april":"april",
    "mei":"may",
    "juni":"june",
    "juli":"july",
    "agustus":"august",
    "september":"september",
    "oktober":"october",
    "nopember":"november",
    "december":"desember"
}
class FormattingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        print(adapter.keys())
        # adapter["hash_id"] = cleanHashText(adapter["nomor"])
        # adapter["scraped_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # adapter["catatan_amar"] = re.sub(r'\s[^a-zA-Z0-9\s-]\s', ' ', adapter["catatan_amar"])
        
        return item