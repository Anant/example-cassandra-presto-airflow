#!/bin/bash

# start presto and cassandra docker containers
docker run -p 8080:8080 --name presto -d ahanaio/prestodb-sandbox
docker run -p 9042:9042 --name cassandra -d cassandra:latest

# install airflow and presto provider
pip install apache-airflow
pip install apache-airflow-providers-presto

airflow db init

airflow users create \
    --username admin \
    --password password \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

airflow webserver --port 7080 &

airflow scheduler &
