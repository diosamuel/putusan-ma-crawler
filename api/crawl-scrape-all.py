from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.demo.spiders.scrape_list_putusan import PutusanPagination
from crawler.demo.spiders.scrape_page import PageInformationScrape

process = CrawlerProcess(get_project_settings())
process.crawl(PageInformationScrape)
process.crawl(PutusanPagination)
process.start()