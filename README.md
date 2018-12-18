# strends-report project readme
Seasonal based reporting of the status and trends of select IEP data

## Instructions


#### Requirements

##### Software

* Python 3.6 or higher (preferably the Anaconda distribution)
* Docker for Windows
* Microsoft Access Database Engine which is available [here](https://www.microsoft.com/en-US/download/details.aspx?id=13255) with instructions [here](https://www.microsoft.com/en-US/download/details.aspx?id=13255)

##### python packages

* pandas
* pyodbc
* psycopg2
* xlrd


#### Docker 

* Install Docker for Windows following the instructions [here](https://docs.docker.com/docker-for-windows/install/)

#### Python

* `cd strends-report`
* `pip install requirements.txt`
* `cd src`

### Usage

* Start a Docker Container that holds persistent storage of the PostfreSQL database by running the shell script,  `./create_strends_data.sh`.

* Initialize a PostGreSQl server by starting a PostgreSQL Docker Container by running the shell script,  `./run_strends_psql.sh`.

* Populate the database with new data using python. For example by running the python script, `inserts.py`.

* Query the PostGreSQl database server in python or R using the `psycopg2` or `Rpostgres` pacakges, respectively.