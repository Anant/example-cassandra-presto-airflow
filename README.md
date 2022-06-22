# Connect Airflow, Presto, and Cassandra

Learn how to connect Airflow, Presto, and Cassandra all on your browser via Gitpod! This demo can also be done on your local via Docker.

## Click below to get started!

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Anant/example-cassandra-presto-airflow)

### 1. Start Presto and Cassandra Docker Containers and install Airflow
**IMPORTANT: Remember to make the ports public when the dialog shows in the bottom righthand corner!**
#### 1.1 Run setup script
```bash
bash setup.sh
```

### 2. Open a new terminal and confirm services are running
#### 2.1 Confirm Docker containers are running
```bash
docker ps
```

#### 2.2 Airflow UI on port 7080 and log in
```bash
username: admin
password: password
```

#### 2.3 Presto UI on port 8080


### 3. Setup Presto Connection in Airflow Admin
#### 3.1 Get IP Address
```bash
hostname -I | awk '{print $2}'
```

#### 3.2 Fill in presto_default connection with the following items and then confirm by testing the connection
```bash
Connection Type: Presto
Host: value copied from 3.1
Schema: remove hive and leave blank
Login: admin
Port: 8080
```

### 4. Create Cassandra Catalog in Presto
#### 4.1 Update {hostname} in cassandra.properties file with value from 3.1
```bash
sed -i "s/{hostname}/$(hostname -I | awk '{print $2}')/" cassandra.properties
```

#### 4.2 Copy cassandra.properties to Presto container
```bash
docker cp cassandra.properties $(docker container ls | grep 'presto' | awk '{print $1}'):/opt/presto-server/etc/catalog/cassandra.properties
```

#### 4.3 Confirm cassandra.properties was moved to Presto container
```bash
docker exec -it presto sh -c "ls /opt/presto-server/etc/catalog"
```

### 5. Confirm Presto CLI can see Cassandra catalog
#### 5.1 Start Presto CLI
```bash
docker exec -it presto presto-cli
```

#### 5.2 Run show command
```bash
show catalogs ;
```
If you do not see cassandra, then we need to restart the container

#### 5.3 Restart Presto container
```bash
docker restart presto
```

#### 5.4 Repeat 5.1 and 5.2 and confirm if you can now see the cassandra catalog

### 6. Set up Cassandra data
#### 6.1 Copy CQL file onto Cassandra Container
```bash
docker cp setup.cql $(docker container ls | grep 'cassandra' | awk '{print $1}'):/
```
#### 6.2 Run CQL file
```bash
docker exec -it cassandra cqlsh -f setup.cql
```

### 7. Run DAGs
#### 7.1 Move DAGs into Dags Folder
```bash
mkdir ~/airflow/dags && mv presto_read_from_cassandra.py ~/airflow/dags && mv presto_join_and_xcom.py ~/airflow/dags && mv presto_write_to_cassandra.py ~/airflow/dags
```
#### 7.2 While waiting on scheduler to pick up Dags, create Presto query variable
##### 7.2.1 Under Airflow Admin in the UI, click variables
##### 7.2.2 Click the blue plus sign to create a variable
##### 7.2.3 Fill in the key and values as below:
```bash
key: presto_query
value: select * from cassandra.demo.spacecraft_journey_catalog;
```
#### 7.3 Confirm scheduler has picked up the DAGs in Airflow UI (might take a couple minutes)
#### 7.4 Enable and Run Read From Cassandra Dag
##### 7.4.1 Click on the logs to visualize the result of the Presto query
#### 7.5 Update the presto_query value to the below in Airflow variables
```bash
select cassandra.demo.spacecraft_journey_catalog.spacecraft_name, cassandra.demo.spacecraft_journey_catalog.summary, cassandra.demo.spacecraft_speed_over_time.speed from cassandra.demo.spacecraft_journey_catalog inner join cassandra.demo.spacecraft_speed_over_time on cassandra.demo.spacecraft_journey_catalog.journey_id = cassandra.demo.spacecraft_speed_over_time.journey_id;
```
#### 7.6 Enable and run Join and XCOM Dag
##### 7.6.1 Click on the logs to visualize the result of the Presto query and see how they change from the first task to the second task
#### 7.7 Enable and run Write to Cassandra Dag
##### 7.7.1 Once completed, check out the logs on the write_to_cassandra task
##### 7.7.2 Confirm writes went through to Cassandra
```bash
docker exec -it cassandra cqlsh -e "select * from demo.spacecraft_journey_summary_and_speed"
```

