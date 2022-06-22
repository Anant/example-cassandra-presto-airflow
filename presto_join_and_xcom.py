import logging
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
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
    'presto_join_and_xcom_dag',
    default_args=default_args,
    description='A simple tutorial DAG with PrestoDB and Cassandra',
    # Continue to run DAG once per hour
    schedule_interval='@daily',
)

def read_from_cassandra():
    ph = PrestoHook()

    # Query PrestoDB
    presto_query = Variable.get("presto_query")

    # Fetch Data
    data = ph.get_records(presto_query)
    return data

read_from_cassandra = PythonOperator(
    task_id='read_from_cassandra',
    provide_context=True,
    python_callable=read_from_cassandra,
    dag=dag,
)

def get_xcoms(task_instance):
    xcoms = task_instance.xcom_pull(task_ids='read_from_cassandra')
    for xcom in xcoms:
        print(xcom)

xcom_task = PythonOperator(
    task_id='xcom_get',
    provide_context=True,
    python_callable=get_xcoms,
    dag=dag,
)

read_from_cassandra >> xcom_task
