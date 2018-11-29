# strends-report project readme
Seasonal based reporting of the status and trends of select IEP data

## Instructions

### Installation

(If running on local machine)

#### Docker 

* Install Docker for Windows following the instructions [here](https://docs.docker.com/docker-for-windows/install/)

#### PostgreSQl

* Install compatable [PostGreSQl](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) `v 10.6`

#### Python

cd into directory

`pip install requirements.txt`

### Usage

3) Initialize a PostGreSQl Docker Container by running the shell script,  `db_int.sh`

4) Populate the database with new data by running the python script, `inserts.py`

5) Spin up the PostGreSQl database by running the shell script, `connect_db.sh` and view the data tables