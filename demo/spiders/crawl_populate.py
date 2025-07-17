import scrapy
from demo.items import PutusanItem
from demo.utils.hash import cleanHashText
import re
import logging
import json

"""

    Massive Crawl Putusan Mahkamah Agung using Depth-First-Search Algorithm
    Direktori 

"""
class PutusanSpider(scrapy.Spider):
    name = "crawl_populate"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    start_urls = [
        "https://putusan3.mahkamahagung.go.id/direktori.html"
    ]
    tree = {}

    def parse(self, response):
        traverseDirektori = response.xpath('(//*[@aria-labelledby="headingOne"])[1]//a/@href').getall()
        for i, link in enumerate(traverseDirektori):
            self.tree[link] = {}
            yield scrapy.Request(
                link, 
                callback=self.parseTraverseKlasifikasi,
                cb_kwargs={'parent_link': link},
                dont_filter=True
            )

    def parseTraverseKlasifikasi(self, response, parent_link):
        traverseKlasifikasi = response.xpath('(//*[@aria-labelledby="headingOne"])[2]//a/@href').getall()
        for level_1 in traverseKlasifikasi:
            if len(level_1) > 0:
                self.tree[parent_link][level_1] = {}
                yield scrapy.Request(level_1, callback=self.parseTraversePengadilan,cb_kwargs={
                    'parent_link':parent_link,
                    'level_1':level_1,
                })
    
    def parseTraversePengadilan(self,response,parent_link,level_1):
        traversePengadilan = response.xpath('(//*[@aria-labelledby="headingOne"])[3]//a/@href').getall()
        for level_2 in traversePengadilan:
            if len(level_2) > 0:
                self.tree[parent_link][level_1][level_2] = {}
                yield scrapy.Request(level_2, callback=self.findYear,cb_kwargs={
                    'parent_link':parent_link,
                    'level_1':level_1,
                    'level_2':level_2
                })

    def findYear(self,response,parent_link,level_1,level_2):
        findUpload = response.xpath('(//*[@aria-labelledby="headingOne"])[4]//a/@href').getall()[-1]
        yield scrapy.Request(findUpload, callback=self.parseTraverseTahun,cb_kwargs={
            'parent_link':parent_link,
            'level_1':level_1,
            'level_2':level_2,
        })

    def parseTraverseTahun(self,response,parent_link,level_1,level_2):
        traverseTahun = set(response.xpath('//tbody/tr/td/a/@href').getall())
        yield {
            "parent_link":parent_link,
            "level_1":level_1,
            "level_2":level_2,
            "final":traverseTahun
        }