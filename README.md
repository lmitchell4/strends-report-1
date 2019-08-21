# strends-report project readme
Seasonal based reporting of the status and trends of select IEP data

## Instructions


#### Requirements

##### Software
* Windows only =(
* [Anaconda Python 3.6+ distribution](https://www.anaconda.com/distribution/) 
* [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
* [Microsoft Access Database Engine](https://www.microsoft.com/en-US/download/details.aspx?id=13255) with instructions [here](https://www.microsoft.com/en-US/download/details.aspx?id=13255)
* [PostgreSQL ODBC Database Drivers](https://ftp.postgresql.org/pub/odbc/versions/msi/psqlodbc_11_00_0000-x64.zip)

##### python 

###### Setup `conda` SSL certificates

 Create a certificates file

1. In windows, open `certmgr`

2. Open Trusted Root Certification Authorities Certificates

3. Open the `Water-RootCA` certificate

4. “Details”

5. “Copy to File…”

6. Click “Next”

7. Select ”Base-64…”

8. Click “Next”

9. Name it “ca-certs”, and place it somewhere you can find it. It will automatically be created as a .cer file. 

* Create a system environmental variable `REQUESTS_CA_BUNDLE` and set the path to your Departments MITM certificate (example: `ca-bundle.cer`)

* Setup conda to reference the certificates file to access packages

`conda config --set ssl_verify "path\to\certificate\file\my_ca-bundle.cer"`

#### python packages (for fetching data and populating the PostgresSQL database)

* `pandas`
* `pyodbc`
* `sqlalchemy`
* `xlrd`

##### R packages (for querying PostgreSQL database and generating plots)

* `dplyr`
* `dbplyr`
* `ggplot2`
* `lubridate`
* `RPostgreSQL`

#### Docker 

* Install Docker for Windows following the instructions [here](https://docs.docker.com/docker-for-windows/install/)

	* Note: You may have to enable hardware virtualization for Docker to work properly. Typically this is accomplished
	in your computers BIOS. Depending on the computer manufactuter, the sytem BIOS may entered by pressing `F10` immediately following 
	computer reboot. Consult your computer systems manual or your IT department for more information.

#### Python

To install python using Anaconda run the following commands at the Anaconda prompt.

1. Navigate to the `strends-report` directory:

	`cd strends-report\strends-report`

2. Create the environment from the `environment.yml` file:

	`conda env create -f environment.yml`

3. Activate the new environment: 

	`conda activate strends`

	
### Usage

1. Start Docker Desktop, if not running on startup.

2. Start a Docker Container that holds persistent storage of the PostgreSQL database by running the shell script:
	
	`./docker/create_strends_data.sh`

3. Initialize a PostgreSQl server by starting a PostgreSQL Docker Container by running the shell script at the bash prompt ($):
	
	`./docker/run_strends_psql.sh`

4. Populate the database with new data using python:

* Run the main script directly 

	`cd src`

	`python main.py`

5. Query the PostgreSQl database server in python using `psycopg2` or R using `dbplyr`.

6. You can connect to the database and generate plots in R by running `drivr.R` located in `\examples`

7. Table names and column names are defined in `tablenames.txt` and `columns.xlsx`, respectively.



#### Docker cheat sheet

* List Docker CLI commands

`docker`

`docker container --help`

* Display Docker version and info

`docker --version`

`docker version`

`docker info`

* List Docker images

`docker image ls`

* List Docker containers (running, all, all in quiet mode)

`docker container ls`

`docker container ls --all`

`docker container ls -aq`

* Stop all docker containers:

	`docker container stop $(docker container ls -aq)`

* Remove all docker containers:

	`docker container rm $(docker container ls -aq)`

* More docker commands:

	```
	docker container ls                                # List all running containers
	docker container ls -a             # List all containers, even those not running
	docker container stop <hash>           # Gracefully stop the specified container
	docker container kill <hash>         # Force shutdown of the specified container
	docker container rm <hash>        # Remove specified container from this machine
	docker container rm $(docker container ls -a -q)         # Remove all containers
	docker image ls -a                             # List all images on this machine
	docker image rm <image id>            # Remove specified image from this machine
	docker image rm $(docker image ls -a -q)   # Remove all images from this machine
	docker login             # Log in this CLI session using your Docker credentials
	docker tag <image> username/repository:tag  # Tag <image> for upload to registry
	docker push username/repository:tag            # Upload tagged image to registry
	docker run username/repository:tag                   # Run image from a registry
	```
	
	
#### Installing docker on MS 2016 (ala Remote Desktop running on a VM)

[Source](https://blogs.technet.microsoft.com/canitpro/2016/10/26/step-by-step-setup-docker-on-your-windows-2016-server/)

1. Open an elevated Windows PowerShell session and run the following commands to install the OneGet PowerShell module. 
 
	`Install-Module -Name DockerMsftProvider -Repository PSGallery -Force`
  
	-Type "Y" to continue
  
2. Next we will install the latest version of Docker using the following command.  when prompted to tell you that the source is untrusted and whether or not you want to continue.  type “A” to continue.
  
	`Install-Package -Name docker -ProviderName DockerMsftProvider`

	-Type "A" to continue
	
3. When the installation is complete, reboot the computer using this PowerShell command.

	`Restart-Computer -Force`