# Putusan Mahkamah Agung Crawler using Scrapy, Apache Airflow, ClickHouse and S3 MinIO

This is a 1+ month internship project that helps telecom companies enrich their user data by scraping Supreme Court decisions (putusan mahkamah agung) and extracting descriptions from them.

## Tech Stack Overview

This project was both challenging and enjoyable to work on.

- **Scrapy**: Handles web crawling and page extraction
- **ClickHouse**: Stores and enables fast querying of crawled data
- **Apache Airflow**: Orchestrates the crawler
- **S3 MinIO**: Data lake for storing PDFs

## Project Structure

```
putusan-ma-crawler/
├── 📁 airflow/                          # Apache Airflow orchestration
│   ├── 📁 config/
│   │   └── 📄 airflow.cfg               # Airflow configuration
│   └── 📁 dags/                         # Airflow DAGs
│       ├── 📄 bulk_crawl.py             # Bulk crawling DAG
│       ├── 📄 latest_putusan.py         # Latest decisions DAG
│       └── 📄 populate_tree.py          # Tree population DAG
├── 📁 api/                              # API endpoints
│   ├── 📄 crawl-scrape-all.py           # Scrape all data API
│   ├── 📄 generate-tree.py              # Generate tree API
│   └── 📄 get-latest-putusan.py         # Get latest decisions API
├── 📁 crawler/                          # Scrapy crawler application
│   ├── 📁 demo/                         # Main Scrapy project
│   │   ├── 📁 spiders/                  # Spider definitions
│   │   │   ├── 📄 crawl_populate.py     # Population spider
│   │   │   ├── 📄 recent.py             # Recent decisions spider
│   │   │   ├── 📄 scrape_list_putusan.py # List scraping spider
│   │   │   └── 📄 scrape_page.py        # Page scraping spider
│   │   ├── 📁 utils/                    # Utility functions
│   │   │   ├── 📁 etl/                  # ETL utilities
│   │   │   │   └── 📄 db.py             # Database operations
│   │   │   ├── 📄 convertDate.py        # Date conversion utilities
│   │   │   └── 📄 hash.py               # Hashing utilities
│   │   ├── 📄 items.py                  # Scrapy item definitions
│   │   ├── 📄 middlewares.py            # Scrapy middlewares
│   │   ├── 📄 pipelines.py              # Scrapy pipelines
│   │   └── 📄 settings.py               # Scrapy settings
│   ├── 📁 plugins/                      # Scrapy plugins
│   ├── 📁 venv/                         # Virtual environment
│   ├── 📄 scrapy.cfg                    # Scrapy configuration
│   └── 📄 uuid                          # UUID file
├── 📁 extract/                          # Data extraction utilities
│   ├── 📄 config.py                     # Extraction configuration
│   ├── 📄 extractor.py                  # Main extractor logic
│   ├── 📄 main.py                       # Extraction entry point
│   └── 📄 url_process.py                # URL processing utilities
├── 📁 img/                              # Project images
│   └── 📄 architecture.png              # System architecture diagram
├── 📄 -docker-compose.yaml              # Alternative docker-compose
├── 📄 -Dockerfile                       # Alternative Dockerfile
├── 📄 .gitignore                        # Git ignore rules
├── 📄 docker-compose.yaml               # Docker Compose configuration
├── 📄 Dockerfile                        # Docker configuration
├── 📄 entrypoint.sh                     # Docker entrypoint script
├── 📄 requirements.txt                  # Python dependencies
└── 📄 README.md                         # Project documentation
```

## Prerequisites
- Python 3.7+
- [Scrapy](https://scrapy.org/)
- [ClickHouse](https://clickhouse.com/)
- [S3 MinIO](https://min.io/)
- [Apache Airflow](https://airflow.apache.org/)

## How to Run

```bash
docker run -d --name airflow \
  --network airflow-net \
  -p 8080:8080 \
  -v ".:/opt/airflow/project" \
  -v "./airflow/dags:/opt/airflow/project/dags" \
  -v "./airflow/plugins:/opt/airflow/project/plugins" \
  -e AIRFLOW_HOME=/opt/airflow/project \
  -e AIRFLOW__CORE__EXECUTOR=SequentialExecutor \
  apache/airflow:3.0.3-python3.10 \
  bash -c "cd /opt/airflow/project && pip install -r requirements.txt && airflow standalone"

docker run -d \
  --network airflow-net \
  --name clickhouse \
  --ulimit nofile=262144:262144 \
  -e CLICKHOUSE_USER=default \
  -e CLICKHOUSE_PASSWORD=default \
  -p 8123:8123 \
  -p 9000:9000 \
  clickhouse/clickhouse-server

docker run -d --name minio \
  -p 9090:9090 \
  -p 9091:9091 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  -v "./minio-data:/data" \
  quay.io/minio/minio server /data --console-address ":9091"
```