# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PutusanItem(scrapy.Item):
    hash_id=scrapy.Field()
    link_detail = scrapy.Field()
    pengadilan = scrapy.Field()
    kategori = scrapy.Field()
    register = scrapy.Field()
    putus = scrapy.Field()
    upload = scrapy.Field()
    nomor_putusan = scrapy.Field()
    tanggal_putusan = scrapy.Field()
    pihak = scrapy.Field()
    views = scrapy.Field()
    downloads = scrapy.Field()


class PageItems(scrapy.Item):
    key = scrapy.Field()
    value = scrapy.Field()