from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="scrapy_manual_trigger",
    start_date=datetime(2025, 7, 24),
    catchup=False,
    tags=["scrapy", "manual"],
) as dag:

    run_scrapy = BashOperator(
        task_id="run_scrapy_direktori",
        bash_command="scrapy crawl direktori",
    )


    webhook = BashOperator(
        task_id="webhook",
        bash_command="curl https://webhook.site/f89bf432-9491-4fab-b9be-3e07b1e64d70?params=success+dunia+akhirat"
    )

    run_scrapy >> webhook