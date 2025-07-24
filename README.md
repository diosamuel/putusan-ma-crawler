# Massive Putusan Mahkamah Agung Crawler

## Architecture
- **Scrapy**: Handles web crawling and data extraction
- **ClickHouse**: Stores and enables fast querying of crawled data

## Prerequisites
- Python 3.7+
- [Scrapy](https://scrapy.org/)
- [ClickHouse](https://clickhouse.com/)

Install Python dependencies:
```bash
pip install -r requirements.txt
```

- **Activate virtual environtment**
```bash
  source venv/bin/activate
```

- **Generate struktur tree putusan Mahkamah Agung**
  ```bash
  scrapy crawl crawl_populate
  ```
  Output: crawl_populate.json

- **Crawl link semua putusan berdasarkan struktur Tree**
  ```bash
  scrapy crawl scrape_list_putusan
  ```
  Output: table `putusan_data`

  **Monitor & scrape direktori terbaru**
  ```bash
  scrapy crawl direktori
  ```
  Output: table `putusan_data`

  - **Scrape semua putusan berdasarkan hasil crawl sebelumnya**
  ```bash
  scrapy crawl scrape_page
  ```
  Output: table `putusan`