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
    'presto_write_to_cassandra_dag',
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

def write_to_cassandra(task_instance):
    xcoms = task_instance.xcom_pull(task_ids='read_from_cassandra')
    ph = PrestoHook()
    for xcom in xcoms:
        # Query PrestoDB
        presto_write_query = f"INSERT INTO cassandra.demo.spacecraft_journey_summary_and_speed (spacecraft_name, summary, speed) VALUES ('{xcom[0]}', '{xcom[1]}', {xcom[2]})"

        # Run query
        # default method
        ph.get_records(presto_write_query)

        # run method
        # ph.run(presto_write_query)

    # insert_rows method using table and iterable tuple    
    # ph.insert_rows("cassandra.demo.spacecraft_journey_summary_and_speed", tuple(value))

write_to_cassandra = PythonOperator(
    task_id='write_to_cassandra',
    provide_context=True,
    python_callable=write_to_cassandra,
    dag=dag,
)

read_from_cassandra >> write_to_cassandra