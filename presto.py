import logging
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from airflow.hooks.presto_hook import PrestoHook

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    }

dag = DAG(
    'presto_dag',
    default_args=default_args,
    description='A simple tutorial DAG with PrestoDB and Spark',
    # Continue to run DAG once per hour
    schedule_interval='@daily',
)

def talk_to_presto():
    ph = PrestoHook()

    # Query PrestoDB
    query = "show catalogs"

    # Fetch Data
    data = ph.get_records(query)
    logging.info(data)
    return data

presto_task = PythonOperator(
    task_id='talk_to_presto',
    provide_context=True,
    python_callable=talk_to_presto,
    dag=dag,
)

presto_task