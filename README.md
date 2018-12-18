# strends-report project readme
Seasonal based reporting of the status and trends of select IEP data

## Instructions


#### Requirements

* Python 3.6 or higher (preferably the Anaconda distribution)
* Docker for Windows
* MS Office

#### Docker 

* Install Docker for Windows following the instructions [here](https://docs.docker.com/docker-for-windows/install/)

#### Python

* `cd strends-report`
* `pip install requirements.txt`
* `cd src`


#### Using pyodbc with python

* Requires  Microsoft Office matching bit version of python  

### Usage

* Start a Docker Container that holds persistent storage of the PostfreSQL database by running the shell script,  `./create_strends_data.sh`

* Initialize a PostGreSQl server by starting a PostgreSQL Docker Container by running the shell script,  `./run_strends_psql.sh`

* Populate the database with new data using python. For example by running the python script, `inserts.py`

* Query the PostGreSQl database server in python or R using 