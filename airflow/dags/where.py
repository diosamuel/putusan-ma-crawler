from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from pendulum import datetime

@dag(
    schedule=None,
    start_date=datetime(2025, 7, 1),
    catchup=False,
    tags=["demo", "putusan"],
)
def check():
    checks = BashOperator(
        task_id="check",
        bash_command="cd /opt/airflow/project && echo $(pwd) && echo here"
    )

checks = check()
