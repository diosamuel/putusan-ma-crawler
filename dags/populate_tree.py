from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from pendulum import datetime

@dag(
    schedule=None,
    start_date=datetime(2025, 7, 1),
    catchup=False,
    tags=["demo", "putusan"],
)
def populate_tree_dag():
    populate_tree = BashOperator(
        task_id="populate_tree",
        bash_command="python -m demo.api.generate-tree"
    )

populate_tree_dag_instance = populate_tree_dag()
