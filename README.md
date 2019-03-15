# strends-report project readme
Seasonal based reporting of the status and trends of select IEP data

## Instructions


#### Requirements

##### Software

* Python 3.6 or higher (preferably the Anaconda distribution)
* Docker for Windows
* Microsoft Access Database Engine which is available [here](https://www.microsoft.com/en-US/download/details.aspx?id=13255) with instructions [here](https://www.microsoft.com/en-US/download/details.aspx?id=13255)

##### python packages (for fetching data and populating the PostgresSQL database)

* `pandas`
* `pyodbc`
* `psycopg2`
* `xlrd`

##### R packages (for generating plots)

* `DBI`
* `RPostgres`
* `ggplot2`
* `lubridate`

#### Docker 

* Install Docker for Windows following the instructions [here](https://docs.docker.com/docker-for-windows/install/)

#### Python

* `cd strends-report`
* `pip install requirements.txt`
* `cd src`
* `python main.py`


### Usage

* Start Docker Desktop, if not running on startup

* Start a Docker Container that holds persistent storage of the PostgreSQL database by running the shell script,  `./create_strends_data.sh`.

* Initialize a PostgreSQl server by starting a PostgreSQL Docker Container by running the shell script,  `./run_strends_psql.sh`.

* Populate the database with new data using python. For example by running the python script, `main.py`.

* Query the PostgreSQl database server in python or R using the `psycopg2` or `Rpostgres` packages, respectively.

* You can connect to the database and generate plots in R by running `drivr.R` located in `\examples`