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

## Some Tips