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

## Usage
Run the following commands from the project root to execute the spiders. Output will be saved in JSON Lines format.

- **Activate virtual environtment**
```bash
  source venv/bin/activate
```

- **Populate Crawl Seeds**
  ```bash
  scrapy crawl crawl_populate
  ```
  _Initializes the crawl with seed URLs or data._

- **Scrape List of Decisions**
  ```bash
  scrapy crawl scrape_list_putusan
  ```
  _Crawls and extracts lists of judicial decisions._

- **Scrape Individual Decision Pages**
  ```bash
  scrapy crawl scrape_page
  ```
  _Extracts detailed data from individual decision pages._

## Contribution
Contributions are welcome. Please open an issue or submit a pull request for any improvements or bug fixes.