from airflow.decorators import dag, task
from datetime import datetime

@dag(
    start_date=datetime(2025,4,1),
    schedule='@daily',
    catchup=False,
    tags=['taskflow']
)

def taskflow()

taskflow()