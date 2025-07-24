from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

# dags_schedule = None  # Set to None for manual trigger, or use a cron string

with DAG(
    dag_id='run_scrapy_docker',
    default_args=default_args,
    catchup=False,
    description='Run my-scrapy-project Docker image via DockerOperator',
) as dag:

    run_scrapy = DockerOperator(
        task_id='run_scrapy_container',
        image='my-scrapy-project',
        api_version='auto',
        auto_remove="never",
        command='get-latest-putusan',
        docker_url='unix://var/run/docker.sock',  # Assumes Airflow has access to Docker socket
        network_mode='backend',  # Matches docker-compose network
        # volumes=['/app:/app'],  # Mounts /app inside the container (adjust if needed)
        environment={
            'CLICKHOUSE_HOST': 'clickhouse',
            'CLICKHOUSE_PORT': '8123',
            'CLICKHOUSE_USER': 'default',
            'CLICKHOUSE_PASSWORD': 'default',
        },
        tty=True,
    ) 