+++
date = "2018-08-04"
title = "Azure SQL DWH Introduction"
+++

One major benefit of Azure SQL DWH is that compute and storage can be scaled up or down independently of each other. So we can shrink or expand or compute resources without having to move data. 

So you can shrink your compute resources on weekends or over night and save costs and spin up more compute during the day to save costs.

As far as I understood from reading Amazon Redshift's documentation, storage and compute are more tightly coupled. So resizing in Redshift means that all data ['is copied in parallel from the compute node or nodes in your source cluster to the compute node or nodes in the target cluster'](https://docs.aws.amazon.com/redshift/latest/mgmt/rs-resize-tutorial.html).

You can also map external data stored in Azure Blob Storage or Azure Datalake into the datawarehouse.

# Designing and Querying Data Warehouses

## Table Distributions

Azure SQL DWH distributes data from each table accross multiple databases so that processing can happen in parallel on a massive scale if needed (MPP: massively parallel processing).

In the example below, we use the column `customerId` to distribute our table on the underlying nodes:
```
CREATE TABLE myTable 
    (
    customerID int NOT NULL,
    lastName varchar(20),
    zipCode varchar(6)
    )
WITH
    (
    CLUSTERED COLUMNSTORE INDEX,
    DISTRIBUTION = HASH([customerId])
    -- Or use:
    -- DISTRIBUTION = ROUND_ROBIN
    )
```


Intuitively, the column you use to distribute the data should partition the data evenly so you can spread the load evenly accross compute nodes. If data is spread unevenly accross nodes, this is commonly called 'data skew'.

If you have no idea about your data distribution, you can use `ROUND_ROBIN` instead of `HASH` to partition your data. This will distribute your data evenly accross nodes, but will incur more I/O if the distribution is suboptimal for your queries. If you choose no distribution type, Azure SQL DWH defaults to `ROUND_ROBIN`.

In order to avoid data movement for small tables (e.g. <1-2GB compressed, such as dimension tables that rarely change), we can also generate replicated tables on each compute node. Replicating a table is done during the `CREATE TABLE` statement:
```
CREATE TABLE dimRepTable (
    ...
)
WITH
(
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
)
```

Altering the distribution of an existing table is not possible at the moment, but you can quickly create a new table in a parallel fashion using:
```
CREATE TABLE dbo.newPartitionTable
(
    ...
)
AS
SELECT *
FROM dbo.oldPartitionTable

DROP dbo.oldPartitionTable

RENAME dbo.newPartitionTable TO dbo.oldPartitionTable
```

Since the same hash values are stored on the same distribution you should pick a column that is likely part of many of your join statements to minimize data movement.

## Partitioning tables

We now have multiple databases where we distribute our data to. Within these databases we can define partitions. Each partition has its own clustered columnstore. This could look like the following:
```
CREATE TABLE dbo.sampleTable
(
    hashColumn,
    DateKey,
    ...
)
WITH 
(
    CLUSTERED COLUMNSTORE INDEX,
    DISTRIBUTION = HASH(hashColumn),
    PARTITION
    (
        DateKey RANGE RIGHT FOR VALUES 
        (                               
                                        --P:1 dates < 2015
            '2015-01-01 00:00:00.0000'  --P:2 2015 < dates < 2016
            ,'2016-01-01 00:00:00.0000' --P:3 2016 <= dates < 2017
            ,'2017-01-01 00:00:00.0000' --P:4 2017 <= dates < 2018
            ,'2018-01-01 00:00:00.0000' --P:5 2018 <= dates
        )
    )
)
```
Note that we defined 4 partitions, but we get one extra: the partition before 2015. So we have n+1 partitions in total.

Microsoft recommends the following when creating partitions:

- Optimal compression and performance for clustered columnstore tables is at about 1m rows per distribution and partition

So this setup starts to shine with large datasets. Partitioning also allows to efficiently switch data between tables with the same partition keys.

## Indexing

There are two ways you can index data:

- Primary data stores
    - Heap = Base row store
    - Clustered Index CI = Base Row Store maintained as a B-Tree
    - Clustered Columnstore Index CCI = Base columnstore
- Secondary data stores
    - Non Clustered Index NCI = Secondary B-Tree index:
        - possible on Heap and CCI
    - Non Clustered Column Store NCCI is NOT supported

CCI is the default in Azure SQL DWH. 

The syntax for CI and CCI is as follows:
```
CREATE TABLE dbo.sampleTable 
(
    ...
)
WITH
(
    CLUSTERED INDEX(someColumn) --vs: CLUSTERED COLUMNSTORE INDEX
    DISTRIBUTION = ROUND_ROBIN  
)
```
The CI orders the table based on the column specified. The CCI is not stored in an ordered way. 

Creating tables with `HEAP` may be best for lots of loads such as staging tables to speed up processing.

## Statistics

statistics are not created automatically and not updated automatically!
SQL Server uses statistics to help optimize the query plan.

best practice: create stats on columns that appear in your queries

## Monitoring Queries

SELECT *
FROM sys.dm_pdw_exec_requests
WHERE [label] like 'searchstring%'

OPTION(LABEL = 'My query label')

labeling best practices:
project : procedure : statement :  comment

## Elastic Query
https://docs.microsoft.com/en-us/azure/sql-data-warehouse/tutorial-elastic-query-with-sql-datababase-and-sql-data-warehouse

# Integrating & Ingesting Data

## Loading Data



# Other
## Polybase
https://docs.microsoft.com/en-us/sql/relational-databases/polybase/polybase-guide?view=sql-server-2017

## Security
Threat detection and auditing should be enabled! They are NOT enabled by default! Auditing retention days = 0 means unlimited retention.