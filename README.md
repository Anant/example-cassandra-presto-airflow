# Connect Airflow, Presto, and Cassandra

Learn how to connect Airflow, Presto, and Cassandra all on your browser via Gitpod! This demo can also be done on your local via Docker.

## Hit the button below to get started!

[![Open in Gitpod](https://github.com/Anant/example-cassandra-presto-airflow)

### 1. Run setup script to Start Presto and Cassandra Docker Containers and install Airflow
**IMPORTANT: Remember to make the ports public when the dialog shows in the bottom righthand corner!**
#### 1.1
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
#### 3.1 Get IP (copy the 2nd one printed)
```bash
hostname -I
```

#### 3.2 Fill in presto_default connection with the following items and then confirm by testing the connection
```bash
Connection Type: Presto
Host: value copied from 3.1
Schema: remove hive and leave blank
Login: admin
Port: 8080
```
