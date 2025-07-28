import scrapy
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from demo.items import DeskripsiPutusanItem
from demo.utils.hash import cleanHashText
import os
import json
import re
import logging
from datetime import datetime
from demo.utils.etl.db import readData,insertPutusan

class PageInformationScrape(scrapy.Spider):
    putusan = {}
    name = "scrape_page"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    start_urls = list(map(lambda x:x[0],readData("link_detail","list_putusan").result_rows))

    custom_settings = {
        'ITEM_PIPELINES': {
            'demo.pipelines.FormattingPipeline': 100,
        },
        'DOWNLOAD_DELAY':10
    }

    def parse(self, response):
        item = DeskripsiPutusanItem()
        url_putusan = response.request.url
        title = response.css("h2 strong::text").get(default="").strip()
        view_count = response.css('div[title="Jumlah view"]::text').get()
        download_count = response.css('div[title="Jumlah download"]::text').get()

        self.handleRelatedPutusan(response)

        # Each putusan has different keys and values, so create a dynamic scraper based on the table's keys and attributes
        for row in response.css("table tr"):
            tds = row.css("td")
            if len(tds) == 2:
                key = tds[0].css("::text").get(default="").strip().replace(":", "").replace(" ","_").lower()
                value = tds[1].xpath("normalize-space(string())").get(default="").strip()
                if key:
                    item[key] = value
        
        item["putusan"] = self.putusan
        item["view"] = view_count
        item["download"] = download_count
        
        file = response.css("#collapseThree a::attr(href)").getall()
        if len(file) != 0:
            item["zip"], item["pdf"] = response.css("#collapseThree a::attr(href)").getall()

        yield {
            "url":url_putusan,
            "title": title,
            "description": item,
        }

    def handleRelatedPutusan(self,response):
        laws = list(set(map(lambda res:re.sub(r':','',res.strip()),response.css("ul.portfolio-meta.nobottommargin")[2].css("::text").getall())))
        if len(laws) > 10: #If the length is greater than 10, the HTML element indicates an overflow and needs to be handled differently depending on the case.
            putusan_type = response.css("ul.portfolio-meta.nobottommargin")[2].css("strong::text").getall()
            
            # 'Putusan' will serve as the separator for the scraped results.
            if 'Putusan' in putusan_type: 
                putusan_type = putusan_type[0:putusan_type.index('Putusan')]
            putusan_type = list(set(list(map(lambda val:re.sub(r":","",val),putusan_type))))

            putusan_number = response.css("ul.portfolio-meta.nobottommargin")[2].css("a[href]::text").getall()
            putusan_link = response.css("ul.portfolio-meta.nobottommargin")[2].css("a[href]::attr(href)").getall()
            
            if 'Putusan' in putusan_number:
                loc = putusan_number.index('Putusan')
                putusan_number = putusan_number[0:loc]
                putusan_link = putusan_link[0:loc]
            
            cleaned_putusan_type = [x.strip() for x in putusan_type if x.strip()]
            cleaned_putusan_number = [x.strip() for x in putusan_number if x.strip()]

            # The output will be two arrays, which are expected to have the same length so they can be paired
            if len(cleaned_putusan_type) == len(cleaned_putusan_number):
                for index in range(len(cleaned_putusan_type)):
                    self.putusan[cleaned_putusan_type[index]] = {
                        "nomor":cleaned_putusan_number[index],
                        "url":putusan_link[index]
                    }
        else:
            for index in range(1,len(laws[1:]),2):
                self.putusan[laws[index]]=laws[index+1]

        return self.putusan