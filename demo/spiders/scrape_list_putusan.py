import scrapy
from demo.items import PutusanItem
from demo.utils.hash import cleanHashText
import re
import logging
import json
import datetime as datetime
from demo.utils.etl.db import insertData

class PutusanPagination(scrapy.Spider):
    currentPage = 1
    lastPage = 1
    name = "scrape_list_putusan"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    start_urls = []

    try:
        with open("crawl_populate.json",'r') as f:
            data = json.loads(f.read())
            for outer in data:
                for inner in data[outer]:
                    deep = data[outer][inner]
                    if len(deep) > 0:
                        nested = list(map(lambda x:x["upload"] if "upload" in x else x,list(deep.values())))
                        res = [item for sublist in nested for item in sublist]
                        start_urls.extend(res)
    except FileNotFoundError as e:
        logging.warning(e)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # replace start_urls with formatted url like this
        # putusan3.mahkamahagung.go.id/direktori/index/pengadilan/.../{year}/page/{current}.html
    
        self.start_urls = list(map(lambda url:url.replace(".html",f"/page/{self.currentPage}.html"),self.start_urls))

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
                
                # Check if upload date is exists
                upload = 'Upload :' in post.css('.small:nth-child(2) strong::text').getall()      
                if upload:
                    uploadText = post.css('.small:nth-child(2)').get().split("Upload :")[1]
                    uploadDateMatch = re.search(r'\b\d{2}-\d{2}-\d{4}\b', uploadText)
                    if uploadDateMatch:
                        # DD-MM-YYYY to YYYY-MM-DD
                        rawDate = datetime.datetime.strptime(uploadDateMatch.group(), "%d-%m-%Y")
                        formmatedDateUpload = rawDate.strftime("%Y-%m-%d")
                        item['upload'] = formmatedDateUpload

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
                
                yield item