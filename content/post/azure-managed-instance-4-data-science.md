+++
date = "2018-10-31"
title = "Azure SQL Server Managed Instance - A Primer for Data Science"
+++

There are a lot of options for data scientists to store data in the Azure cloud. In this blog post I will cover the pros and cons of Azure SQL Server Managed Instance and will provide a few tips so you can hit the ground running if you decide to take it for a test drive.

## Overview
Azure SQL Server Managed Instance is a hosted version of the 'classic' SQL Server from Microsoft in the Azure cloud that is designed to allow an almost (!) seamless switch from SQL Server installed on-premise. It supports VNET integration, which is a hard requirement at the company I work for. 

Some of the most important pros are:

- Allows resizing with the click of a button: You can increase compute power and storage with a few clicks
- No patching or management of the underlying infrastructure is required
- Almost full feature parity with 'classic' SQL Server
- License is included price and there is an option to get significant savings if you qualify for Azure Hybrid Pricing

However, there are some shortcomings:

- Compared to alternatives such as MariaDB and Postgres the price is still quite high
- No support for Polybase, a service that allows you to map files from Azure Blob or Datalake etc into your database as external tables
- No full feature parity to 'classic' SQL Server. Check out this [link](https://docs.microsoft.com/en-us/azure/sql-database/sql-database-features) for a full comparison of feature availability.

The lack of Polybase support was a bit of a bummer for our team. We wanted to store old tables cheaply in Azure Blob storage and map them into our SQL Managed Instance, but that is not possible at the moment.

Still, the ability to easily scale our server was a huge plus so we decided to give it a go. 

In the next sections I want to give you a few tips on how to work with SQL Server Managed Instance.

## Authentication 

You need to specify an Active Directory admin user in the Azure portal. Azure Active Directory authentication requires database users to be created as contained db users, which means that the user does not have a login in the master database. To create a new contained database user, you need at least `ALTER ANY USER` permissions and run the following code:

```
CREATE USER <AD-USER-NAME> FROM EXTERNAL PROVIDER;
```

Don't forget to assign your new user appropriate permissions after creation:

```
GRANT <permission> ON <object> TO <user>
```

Unlike in 'classic' SQL Server you do not need to create a separate database login to allow access to the server since access is handled by AAD.

## Connecting

In this section I want to briefly cover how to connect to your Managed Instance (MI) using ODBC, SSMS and SSMS with linked server.

### SSMS
Since MI relies on Azure Active Directory you need to upgrade SSMS to version 17.9 or higher. After you upgraded, you will see a new authentication option called *Active Directory: integrated*. Just select this option instead of *Windows-Authentication* and you are ready to go:)

### Linked Server
Before we can create a linked server in SSMS, we are going to create an ODBC connection profile. On Windows 10, simply search for *ODBC Data Source Administrator* or *ODBC Datenquellen einrichten (64bit)* with German language settings. Launch the program with your admin account.

> Note: If you create a 64bit ODBC profile you also have to use the 64bit SQL Import/Export Wizard!

After launching the wizard you need to add a connection profile on the `System-DSN` tab and select the ODBC Driver for SQL Server.

![ODBC-Sys-DSN](../../static/img/odbc-system-dsn.PNG)

If you do not see the ODBC Driver listed here, you need to head to Microsoft's download center to install it first. Then you simply need to follow the setup wizard. 

> Important: Jot down the name of your profile somewhere, we are going to need that later to reference the connection.

When the wizard asks you how you want to authenticate with your database, select *With integrated Active Directory Authentication* and that is it. You can also specify a default database to connect to.




Creating a linked server is quite easy in SSMS:

If you want to connect using ODBC


From R

From SSMS

## Copying data

- linked server
- sql server import export wizard
