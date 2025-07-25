from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from pendulum import datetime

@dag(
    schedule=None,
    start_date=datetime(2025, 7, 1),
    catchup=False,
    tags=["demo", "putusan"],
)
def bulk_crawl():
    bulk_crawl = BashOperator(
        task_id="bulk_crawl",
        bash_command="python -m demo.api.crawl-scrape-all"
    )

bulk_crawl_instance = bulk_crawl()
