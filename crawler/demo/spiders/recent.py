import scrapy
import os
import sys
import re
import logging
import json
import datetime as datetime
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from demo.items import PutusanItem
from demo.utils.hash import cleanHashText
from demo.utils.etl.db import insertData

"""
Crawl recently putusan MA and store it into list_putusan
"""
class Direktori(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY':random.randrange(6,10)
    }
    stop_crawling = False
    currentPage = 1
    lastPage = 1
    name = "direktori"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
    start_urls = [
        f"https://putusan3.mahkamahagung.go.id/direktori/index/page/{currentPage}.html"
    ]

    def parse(self,response):
        checktotalPage = response.css('.pagination.justify-content-center a::attr(href)').getall()
        if len(checktotalPage) < 1:
            self.lastPage = 1
        else:
            totalPage = int(checktotalPage[-1].split('/')[-1].split('.html')[0])
            self.lastPage = totalPage

        if self.currentPage < self.lastPage:
            posts = response.css('#tabs-1 #popular-post-list-sidebar .spost')
            for post in posts:
                item = PutusanItem()
            
                upload = 'Upload :' in post.css('.small:nth-child(2) strong::text').getall()      
                if upload:
                    uploadText = post.css('.small:nth-child(2)').get().split("Upload :")[1]
                    uploadDateMatch = re.search(r'\b\d{2}-\d{2}-\d{4}\b', uploadText)
                    if uploadDateMatch:
                        # DD-MM-YYYY to YYYY-MM-DD
                        rawDate = datetime.datetime.strptime(uploadDateMatch.group(), "%d-%m-%Y")
                        formmatedDateUpload = rawDate.strftime("%Y-%m-%d")
                        item['upload'] = formmatedDateUpload
                        
                        if item['upload'] and item['upload'] < self.CURRENT_DATE:
                            # if Outdated
                            self.stop_crawling = True
                            break

                title_elem = post.css('strong a')
                title_href = title_elem.css('::attr(href)').get()
                item['link_detail'] = response.urljoin(title_href)
                
                title_text = post.css('strong a::text').get()
                if title_text:
                    parts = title_text.split("Nomor")
                    item['nomor'] = parts[1].strip() if len(parts) > 1 else ''
                    item['hash_id'] = cleanHashText(item['nomor'])

                info_text = post.css('div > div:nth-child(4)::text').get()
                if info_text:
                    lines = info_text.strip().split('—')
                    item['tanggal_putusan'] = lines[0].replace('Tanggal', '').strip()

                item["page"] = self.currentPage
                item["scraped_at"] = datetime.datetime.now().strftime("%c")
                try:
                    insertData(item, 'list_putusan', ['upload', 'link_detail', 'nomor','hash_id','page','scraped_at'])
                except Exception as e:
                    logging.error(f"SQL Error: {str(e)}")
                    raise Exception(f"Failed to insert data into database: {str(e)}")
            if not self.stop_crawling and self.currentPage < self.lastPage:
                self.currentPage += 1
                next_page = f"https://putusan3.mahkamahagung.go.id/direktori/index/page/{self.currentPage}.html"
                yield scrapy.Request(next_page, callback=self.parse)