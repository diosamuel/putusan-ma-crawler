from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from pendulum import datetime

@dag(
    schedule=None,
    start_date=datetime(2025, 7, 1),
    catchup=False,
    tags=["demo", "putusan"],
)
def url_to_pdf():
    s3_execute = BashOperator(
        task_id="url-to-pdf",
        bash_command="cd /opt/airflow/project && python -m extract.main"
    )

s3_execute = url_to_pdf()
