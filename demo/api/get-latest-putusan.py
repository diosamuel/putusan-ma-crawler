from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from demo.spiders.recent import Direktori

process = CrawlerProcess(get_project_settings())
process.crawl(Direktori)
process.start()