# Massive Putusan Mahkamah Agung Crawler

## Overview
This project is a scalable web crawler designed to collect and process judicial decisions (putusan) from the Supreme Court of Indonesia (Mahkamah Agung). It leverages a Depth-First-Search (DFS) algorithm, Scrapy for web crawling, and ClickHouse for high-performance data storage. The system is designed for extensibility and integration with workflow orchestration tools such as Apache Airflow.

## Features
- Efficient crawling using DFS to traverse large datasets
- Modular Scrapy spiders for different stages of data collection
- Output in JSON Lines format for easy downstream processing
- Integration-ready with ClickHouse for analytics and storage
- Designed for automation with Airflow or similar schedulers

## Architecture
- **Scrapy**: Handles web crawling and data extraction
- **ClickHouse**: Stores and enables fast querying of crawled data
- **Airflow**: (Optional) Orchestrates and schedules crawling workflows

## Prerequisites
- Python 3.7+
- [Scrapy](https://scrapy.org/)
- [ClickHouse](https://clickhouse.com/)
- (Optional) [Apache Airflow](https://airflow.apache.org/)

Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the following commands from the project root to execute the spiders. Output will be saved in JSON Lines format.

- **Populate Crawl Seeds**
  ```bash
  scrapy crawl crawl_populate -o crawl_populate.jsonl -s FEED_OVERWRITE=True
  ```
  _Initializes the crawl with seed URLs or data._

- **Scrape List of Decisions**
  ```bash
  scrapy crawl scrape_list_putusan -o scrape_list_putusan.jsonl -s FEED_OVERWRITE=True
  ```
  _Crawls and extracts lists of judicial decisions._

- **Scrape Individual Decision Pages**
  ```bash
  scrapy crawl scrape_page -o scrape_page.jsonl -s FEED_OVERWRITE=True
  ```
  _Extracts detailed data from individual decision pages._

## Directory Structure
```
├── demo/                  # Main Scrapy project
│   ├── spiders/           # Scrapy spiders
│   ├── utils/             # Utility modules
│   ├── items.py           # Item definitions
│   ├── pipelines.py       # Data pipelines
│   └── settings.py        # Scrapy settings
├── data/                  # Data output and system files
├── metadata/              # Database schema files
├── preprocessed_configs/  # Preprocessing configs
├── store/                 # Storage for crawled data
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── test.py                # Test scripts
```

## Contribution
Contributions are welcome. Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or support, please contact the project maintainer at [your-email@example.com].
