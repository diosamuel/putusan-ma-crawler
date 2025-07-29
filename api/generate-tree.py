from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.demo.spiders.crawl_populate import GenerateTree

process = CrawlerProcess(get_project_settings())
process.crawl(GenerateTree)
process.start()