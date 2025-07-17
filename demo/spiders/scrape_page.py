import scrapy
# from demo.items import PageItems
from demo.utils.hash import cleanHashText
import os
import json
import re
import logging

class PutusanSpider(scrapy.Spider):
    data = []
    name = "scrape_page"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    start_urls = []
    try:
        with open("scrape_list_putusan.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                start_urls.append(obj["link_detail"])
    except Exception as e:
        logging.warning(e)

    custom_settings = {
        'ITEM_PIPELINES': {
            'demo.pipelines.PagesPipeline': 300,
        }
    }

    def parse(self, response):
        urlPutusan = response.request.url
        title = response.css("h2 strong::text").get(default="").strip()
        data = {}
        for row in response.css("table tr"):
            tds = row.css("td")
            if len(tds) == 2:
                key = tds[0].css("::text").get(default="").strip().replace(":", "")
                value = tds[1].xpath("normalize-space(string())").get(default="").strip()
                if key:
                    data[key] = value

        yield {
            "url":urlPutusan,
            "title": title,
            "data": data,
        }