# Connect Airflow, Presto, and Cassandra

Learn how to connect Airflow, Presto, and Cassandra all on your browser via Gitpod! This demo can also be done on your local via Docker.

## Click below to get started!

[Open in Gitpod](https://github.com/Anant/example-cassandra-presto-airflow)

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

#### 5.3 Repeat 5.1 and 5.2 and confirm if you can now see the cassandra catalog

### 6. Run Airflow Presto Dag
#### 6.1 Move DAG into Dags Folder
```bash
mkdir ~/airflow/dags && mv presto.py ~/airflow/dags
```
#### 6.2 While waiting on scheduler to pick up Dag, create Presto query variable
##### 6.2.1 Under Airflow Admin in the UI, click variables
##### 6.2.2 Click the blue plus sign to create a variable
##### 6.2.3 Fill in the key and values as below:
```bash
key: presto_query
value: show catalogs;
```
#### 6.3 Confirm scheduler has picked up Presto Dag in Airflow UI (might take a couple minutes)
#### 6.4 Enable and run Presto dag
#### 6.5 Review Logs and confirm query returned same thing as we saw with `show catalogs`
#### 6.6 Update the Presto query variable value to `show schemas in cassandra;`
#### 6.7 Rerun dag and confirm that the returned values match the default keyspaces that exist in Cassandra
