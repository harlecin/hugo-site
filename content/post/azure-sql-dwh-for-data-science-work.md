+++
date = "2018-08-04"
title = "Azure SQL DWH - Overview"
+++

There are a multitude of options when it comes to storing and processing data. In this post I want to give you a brief overview of Azure SQL datawarehouse, Microsoft's datawareshouse solution for the Azure cloud and its answer to Amazon Redshift on AWS. 

I will start of by talking briefly about its technical architecture before moving on to cover some of its main features and functionality.

# Technical Architecture

Azure SQL DWH is a MPP datawarehouse, meaning it uses massively parallel procesing to speed up queries. Work is distributed between 1 - 60 compute nodes, depending on your sizing. 

So what can you get performance wise? That is unfortunately not that easy to answer.
Microsoft along with other IT vendors (looking at you IBM) has the annoying habit of combining multiple performance characteristics like CPU, RAM, I/O into some arcane metric that they use to charge you money. In this case, they use Data Warehouse Units (DWUs), or compute DWUs (cDWUs) for generation 2. According to Microsoft's documentation, an increase in DWUs ['linearly changes the performance of the system for scans, aggregations and CTAS statements'](https://docs.microsoft.com/en-us/azure/sql-data-warehouse/what-is-a-data-warehouse-unit-dwu-cdwu)

One major benefit of Azure SQL DWH is that compute and storage can be scaled up or down independently of each other. So we can shrink or expand or compute resources without having to move data. 

This allows you to shrink compute resources on weekends or over night or spin up more compute during the day thereby reducing costs.

As far as I understood from reading Amazon Redshift's documentation, storage and compute are more tightly coupled. So resizing in Redshift means that all data ['is copied in parallel from the compute node or nodes in your source cluster to the compute node or nodes in the target cluster'](https://docs.aws.amazon.com/redshift/latest/mgmt/rs-resize-tutorial.html).

You can also map external data stored in Azure Blob Storage or Azure Datalake into Azure SQL DWH using Polybase (which at the time of this writing is not available for SQL Server managed instances).

One thing to keep in mind is that Azure SQL DWH has a rather low limited for concurrent queries. For generation 2 you start with 32 and go up to a maximum of 128 concurrent queries (see [here](https://docs.microsoft.com/en-us/azure/sql-data-warehouse/memory-and-concurrency-limits) for more details). We are currently evaluating whether that is actually an issue in practice and I will post an update as soon as we get some time to try it.

So, let's dive into some of the technical features: 

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

Altering the distribution of an existing table is not possible at the moment, but you can quickly create a new table in a parallel fashion using the CTAS, i.e. 'CREATE TABLE AS', statement:
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

Since the same hash values are stored on the same distribution you should pick a column that is likely to be part of many of your join statements to minimize data movement.

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

Statistics help the query optimizer to decide which execution plan to choose so they have a large impact on performance.

You can check whether automatic statistic generation is enabled by running:

```
SELECT name, is_auto_create_stats_on 
FROM sys.databases
```

If it is not yet enabled, you can active it by executing:
```
ALTER DATABASE <yourdatawarehousename> 
SET AUTO_CREATE_STATISTICS ON
```
Automatic statistic generation is triggered by SELECT, INSERT-SELECT, CTAS, UPDATE, DELETE, and EXPLAIN (in certain cases).

Microsoft recommends to update statistics for date columns each day as new dates are added, but statistics say on slowly moving dimensions such as sales region might never have to be updated. You should focus on columns used in joins, groupings, orderings etc.

So if your queries are slow, you might want to check if your statistics are still up-to-date.

You can manually create statistics like so:
```
CREATE STATISTICS [statistics_name] ON [schema_name].[table_name]([column_name1],[column_name2] ) WITH SAMPLE = 30 PERCENT
```
The `WITH SAMPLE` part is optional and it defaults to 20% if not specified otherwise. You can use stored procedures with dynamic sql to loop through tables and columns.

Updating is as simple as:
```
# specific update
UPDATE STATISTICS [schema_name].[table_name]([stat_name]);

# all statistics
UPDATE STATISTICS [schema_name].[table_name];
```



## Monitoring Queries

Sometimes you need to troubleshoot queries. In order to make it easier to find specific queries you can use `LABEL` to give them a name:
```
SELECT *
FROM someTable
OPTION (LABEL = 'My Label')
```

Then run the following to find your query:
```
SELECT *
FROM sys.dm_pdw_exec_requests
WHERE [label] like 'searchstring%'
```

If there are lots of queries, it might be useful to adopt a labeling convention such as this one:
```
project : procedure : statement :  comment
```

## Elastic Query

Elastic query allows you to query Azure SQL DWH from an SQL Server database by adding a datawarehouse table as an external data source. You can find a tutorial [here](https://docs.microsoft.com/en-us/azure/sql-data-warehouse/tutorial-elastic-query-with-sql-datababase-and-sql-data-warehouse). 


## Polybase

You can use Polybase to map data stored in Azure Blob storage or Azure Datalake into your datawarehouse as an external table. For more information on Polybase, click [here](https://docs.microsoft.com/en-us/sql/relational-databases/polybase/polybase-guide?view=sql-server-2017)

Last, but not least a word on security:

## Security
Threat detection and auditing are not enabled by default. They incur extra charges, but this is definitely something that you should look into. If you specify 'Auditing retention days = 0' audit logs are kept indefinitely.

I hope you liked the post:) If you find any erros etc, I would ask you to open an issue on Github.