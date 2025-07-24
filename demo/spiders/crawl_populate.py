import scrapy
import re
import logging
import json

class GenerateTree(scrapy.Spider):
    name = "crawl_populate"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    start_urls = [ "https://putusan3.mahkamahagung.go.id/direktori.html" ]
    tree = {}
    def parse(self, response):
        traverseDirektori = response.xpath('(//*[@aria-labelledby="headingOne"])[1]//a/@href').getall()
        for i, direktori in enumerate(traverseDirektori):
            if direktori != "https://putusan3.mahkamahagung.go.id/direktori.html":
                self.tree[direktori] = {}
                yield scrapy.Request(
                    direktori, 
                    callback=self.parseTraverseKlasifikasi,
                    cb_kwargs={'direktori': direktori},
                )

    def parseTraverseKlasifikasi(self, response, direktori):
        traverseKlasifikasi = response.xpath('(//*[@aria-labelledby="headingOne"])[2]//a/@href').getall()
        for klasifikasi in traverseKlasifikasi:
            if len(klasifikasi) > 0:
                self.tree[direktori][klasifikasi] = {}
                yield scrapy.Request(klasifikasi, callback=self.parseTraversePengadilan,cb_kwargs={
                    'direktori':direktori,
                    'klasifikasi':klasifikasi,
                })
    
    def parseTraversePengadilan(self,response,direktori,klasifikasi):
        traversePengadilan = response.xpath('(//*[@aria-labelledby="headingOne"])[3]//a/@href').getall()
        for pengadilan in traversePengadilan:
            if len(pengadilan) > 0:
                self.tree[direktori][klasifikasi][pengadilan] = {}
                yield scrapy.Request(pengadilan, callback=self.findYear,cb_kwargs={
                    'direktori':direktori,
                    'klasifikasi':klasifikasi,
                    'pengadilan':pengadilan
                })

    def findYear(self,response,direktori,klasifikasi,pengadilan):
        findUpload = response.xpath('(//*[@aria-labelledby="headingOne"])[4]//a/@href').getall()[-1] # get last value
        yield scrapy.Request(findUpload, callback=self.parseTraverseTahun,cb_kwargs={
            'direktori':direktori,
            'klasifikasi':klasifikasi,
            'pengadilan':pengadilan,
        })

    def parseTraverseTahun(self,response,direktori,klasifikasi,pengadilan):
        traverseTahun = set(response.xpath('//tbody/tr/td/a/@href').getall())
        self.tree[direktori][klasifikasi][pengadilan]["upload"] = list(traverseTahun)
        
        with open("crawl_populate.json","w") as f:
            f.write(json.dumps(self.tree))
        
        yield {
            "direktori":direktori,
            "klasifikasi":klasifikasi,
            "pengadilan":pengadilan,
            "upload":traverseTahun
        }