from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from pendulum import datetime

@dag(
    schedule=None,
    start_date=datetime(2025, 7, 1),
    catchup=False,
    tags=["demo", "putusan"],
)
def latest_putusan():
    run_get_latest_putusan = BashOperator(
        task_id="run_get_latest_putusan",
        bash_command="python -m demo.api.get-latest-putusan"
    )

populate_tree_dag_instance = latest_putusan()
