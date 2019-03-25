# strends-report project readme
Seasonal based reporting of the status and trends of select IEP data

## Instructions


#### Requirements

##### Software

* [Anaconda Python 3.6+ distribution](https://www.anaconda.com/distribution/) 
* [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
* [Microsoft Access Database Engine](https://www.microsoft.com/en-US/download/details.aspx?id=13255) with instructions [here](https://www.microsoft.com/en-US/download/details.aspx?id=13255)

##### python packages (for fetching data and populating the PostgresSQL database)

* `pandas`
* `pyodbc`
* `psycopg2`
* `xlrd`

##### R packages (for querying data and generating plots)

* `dplyr`
* `dbplyr`
* `ggplot2`
* `lubridate`

#### Docker 

* Install Docker for Windows following the instructions [here](https://docs.docker.com/docker-for-windows/install/)

#### Python

To install python using Anaconda run the following commands at the Anaconda prompt

1. Create the environment from the `environment.yml` file:

	`conda env create -f environment.yml`

2. Activate the new environment: 

	`conda activate strends`

### Usage

1. Start Docker Desktop, if not running on startup.

2. Start a Docker Container that holds persistent storage of the PostgreSQL database by running the shell script:
	
	`.$ /create_strends_data.sh`.

3. Initialize a PostgreSQl server by starting a PostgreSQL Docker Container by running the shell script:
	
	`$ ./run_strends_psql.sh`.

4. Populate the database with new data using python. For example by running the python script, `main.py`.

5. Query the PostgreSQl database server in python using `psycopg2` or R using `dbplyr`.

6. You can connect to the database and generate plots in R by running `drivr.R` located in `\examples`

7. Table names and column names are defined in `tablenames.txt` and `columns.xlsx`, respectively.

#### Helpful commands to manage docker instances:

* Stop all docker containers:

	`$ docker container stop $(docker container ls -aq)`

* Remove all docker containers:

	`$ docker container rm $(docker container ls -aq)`