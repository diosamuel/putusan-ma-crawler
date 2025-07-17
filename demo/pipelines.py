# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from demo.utils.hash import cleanHashText
# import pendulum as pm

class DemoPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "hash_id" in adapter.keys():
            adapter['hash_id'] = cleanHashText(adapter['nomor_putusan']+adapter["register"])
            # for dateAdapter in ["register","putus","upload"]:
                # adapter[dateAdapter] = pm.from_format(adapter[dateAdapter],"DD-MM-YYYY").to_date_string()
        return item


class PagesPipeline:
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
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        return item