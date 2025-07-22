"""
    The Pagination
"""
import scrapy
from demo.items import PutusanItem
from demo.utils.hash import cleanHashText
import re
import logging
import json
import datetime as datetime

class Direktori(scrapy.Spider):
    currentPage = 1
    lastPage = 1
    name = "direktori"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'demo.pipelines.FormattingPipeline': 100,
        }
    }
    
    start_urls = ["https://putusan3.mahkamahagung.go.id/direktori.html"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # replace start_urls with formatted url like this
        # putusan3.mahkamahagung.go.id/direktori/index/pengadilan/.../{year}/page/{current}.html
    
        self.start_urls = list(map(lambda url:url.replace(".html",f"/page/{self.currentPage}.html"),self.start_urls))

    def parse(self,response):
        logging.debug(response.request.url)
        checktotalPage = response.css('.pagination.justify-content-center a::attr(href)').getall()
        if len(checktotalPage) < 1:
            self.lastPage = 1
        else:
            totalPage = int(checktotalPage[-1].split('/')[-1].split('.html')[0])
            self.lastPage = totalPage

        if self.currentPage < self.lastPage:
            self.currentPage += 1
            posts = response.css('#popular-post-list-sidebar .spost')
            for post in posts:
                item = PutusanItem()
                title_elem = post.css('strong a')
                title_href = title_elem.css('::attr(href)').get()
                item['link_detail'] = response.urljoin(title_href)
                breadcrumbs = post.css('.small:nth-child(1) a::text').getall()
                item['pengadilan'] = breadcrumbs[1] if len(breadcrumbs) > 1 else ''
                item['kategori'] = breadcrumbs[2] if len(breadcrumbs) > 2 else ''
                dates = post.css('.small:nth-child(2)::text').getall()
                dates_clean = [x.strip('— \n\t') for x in dates if x.strip()]
                item['register'] = dates_clean[0].replace('Register :', '').strip()
                item['putus'] = dates_clean[1].replace('Putus :', '').strip()
                item['upload'] = dates_clean[2].replace('Upload :', '').strip()

                title_text = post.css('strong a::text').get()
                if title_text:
                    parts = title_text.split("Nomor")
                    item['nomor'] = parts[1].strip() if len(parts) > 1 else ''

                info_text = post.css('div > div:nth-child(4)::text').get()
                if info_text:
                    lines = info_text.strip().split('—')
                    item['tanggal_putusan'] = lines[0].replace('Tanggal', '').strip()
                    item['pihak'] = lines[1].strip() if len(lines) > 1 else ''

                item['view'] = post.css('i.icon-eye + strong::text').get(default='0')
                item['download'] = post.css('i.icon-download + strong::text').get(default='0')
                 
                yield item