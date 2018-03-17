+++
date = "2018-03-13"
title = "Running Microsoft SQL 2017 in Docker on Redhat"
+++

## Install Docker on Redhat
As per the documentation here, you can install Docker CE 17.03 (or future versions) on RHEL 7.3 64-bit via:

Set up the Docker CE repository on RHEL:

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum makecache fast
Install the latest version of Docker CE on RHEL:

sudo yum -y install docker-ce
Alternatively, you can specify a specific version of Docker CE:

sudo yum -y install docker-ce-<version>-<release>
Start Docker:

sudo systemctl start docker
Test your Docker CE installation:

sudo docker run hello-world
Source: https://stackoverflow.com/questions/42981114/install-docker-ce-17-03-on-rhel7

## Get Image
Source: https://hub.docker.com/r/microsoft/mssql-server-linux/

Description

create Docker group to avoid sudo


## Setup Server
Run docker container:
```
sudo docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=your-super-strong-password-here' --name "mssql" -p 1433:1433 -d microsoft/mssql-server-linux:2017-latest
```

## Managing your SQLS
Source: https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker#connectexternal

SQLS Management Studio: IP,Port (!!!)

Attention: stopping and removing a container permanently deletes any SQL Server data in the container
```
docker stop mssql
docker rm mssql
```

## R code
> library(RODBC)
> odbcConnect("SQLServer") 
 

odbcConnect("SQL", uid="SA", pwd = "yourStrong(!)Password") 
 

bzw con = odbcConnect("SQL", uid="SA", pwd = "yourStrong(!)Password") 

## Auto-restart

[1] https://docs.docker.com/install/linux/linux-postinstall//

[2] https://docs.docker.com/engine/reference/run/#restart-policies---restart



Data-backup: https://docs.microsoft.com/en-us/sql/linux/tutorial-restore-backup-in-sql-server-container

Change Docker-Port: https://stackoverflow.com/questions/19335444/how-do-i-assign-a-port-mapping-to-an-existing-docker-container

