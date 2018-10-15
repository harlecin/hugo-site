+++
date = "2018-07-08"
title = "More advanced SQL Server for Data Scientists"
+++

In the previous post I covered the basics you need to know to work with SQL Server. In this post, I want to show you some more advanced techniques that I found pretty helpful.

The topics I will cover include:

- How to speed up your queries with indices and using columnstore
- Using `Views` and `Table Variables` to make working with complex queries easier
- Introduction to working with functions and stored procedures
- Grouping sets and pivoting data
- Programming and error handling
- Collaborating on a database project and version control

## Indices and columnstore tables

You have probably already heard the following quite a lot:

> Our queries are slow, we need to add an index

Creating indices is more or less synonymous for speeding up queries. A well indexed table allows the database to find relevant entries faster and thereby to speed up query processing.

Creating indices is pretty simple in SQL Server, all you need to do is:
```
-- non-clustered index
CREATE INDEX indexName on tableName (columnName)

-- clustered index
CREATE CLUSTERED INDEX indexName on tableName (columnName)
```

A clustered index physically reorders the corresponding rows in a table and therefore only one clustered index per table is possible.

If your queries are still slow, you can change your table from rowstore to columnstore format. Saving your information in columnstore format allows the database to efficiently compress information along columns and thereby reducing the memory footprint. Moreover, extracting subsets of data is faster, because you do not need to consider unnecessary columns.

Creating a columnstore index is as simple as:
```
-- non-clustered index
CREATE COLUMNSTORE INDEX indexName ON tableName

-- clustered index
CREATE CLUSTERED COLUMNSTORE INDEX indexName ON tableName
```

As a rule of thumb, columnstore indices work best for analytical workloads and rowstore indices for transactional workloads


Please note that while creating an index is simple, working effectively with indices is usually not. There are many nuances and different index types, so if you want to get maximum performance I recommend to talk to a database developer or be prepared to read quite some online documentation:)

## Views & Table Variables

Views are simply named queries that we can interact with as if they were normal tables. We are 'viewing' through the view into the tables underneath.

Creating a view is as simple as:
```
CREATE VIEW dbo.vTestData
AS 
SELECT *
FROM dbo.SomeTable
WHERE col1 = '1'
```

Now we have a view called `dbo.vTestData` that shows us all entries from `dbo.SomeTable` where `col1 = '1'`.

We can now query this view as we would a normal table:
```
SELECT *
FROM dbo.vTestData
```

Table variables can be created by running:
```
DECLARE @varSomeName table
(
col1 INTEGER,
col2 VARCHAR(10)
)

INSERT INTO @varSomeName (col1, col2)  
VALUES (1, 'asdf'),
       (2, 'jklö')

SELECT * 
FROM @varSomeName
```
Table variables should only be used on very small datasets and are only available during execution of the query (in contrast to temp tables).

## Table-valued functions and stored procedures

To create a table-valued function (TVF) run:
```
CREATE FUNCTION dbo.fn_FilterID(@id AS INTEGER)
RETURNS TABLE
AS
RETURN
(SELECT *
FROM dbo.SomeTable
WHERE id = @id)

SELECT *
FROM FilterID(1) as FilterID
```

So a TVF is in a sense a parameterized view.

### Stored Procedures
Before we start with stored procedures, we briefly need to talk about batches:

A batch is a set of commands sent to SQLS as one block. They determine variable and name scope. SQL Server uses `GO [n]` to specify the number of times a batch should be executed.

You can declare and use variables like so:
```
DECLARE @variable NVARCHAR(15) = 'asdf'

-- change variable
SET @variable = 'jklö'

SELECT *
FROM dbo.SomeTable
WHERE col1 = @variable
```

Now let's create a stored procedure and run it:
```
CREATE PROCEDURE dbo.TestProcedure(@variable NVARCHAR(15) = NULL) AS
BEGIN
    IF @variable IS NULL
        PRINT 'variable is NULL'
    ELSE
        PRINT @variable

    -- exit success
    RETURN 0
END

-- Execute the stored procedure with parameter:
EXEC dbo.TestProcedure 'test'

-- Without parameter:
EXEC dbo.TestProcedure

-- save output to variable
DECLARE @return_status INT
EXEC @return_status = dbo.TestProcedure
SELECT 'Return Status' = @return_status
```
Note that we did not put the parameter in parenthesis in order to pass it to the stored procedure. Replace `CREATE` with `ALTER` to change or update an existing stored procedure. Parenthesis in the `CREATE PROCEDURE` statement are optional. You could also define a procedure with variables like so:
```
CREATE PROCEDURE dbo.TestProcedure    
    @variable NVARCHAR(50),   
    @someOtherVariable NVARCHAR(50)
AS
BEGIN
...
END
```

## Grouping sets and pivoting data

### Grouping sets
When we use `GROUP BY` to aggregate data, we only get one specific aggregation level back. But suppose we want to group our data by different levels of aggregation, how could we do that?

One simple way is to use `GROUPING SETS`:
```
SELECT col1
    ,col2
    ,SUM(col3) AS SumTotal
FROM dbo.SomeTable
GROUP BY
GROUPING SETS(
    col1        -- SumTotal grouped by col1
    ,col2       -- SumTotal grouped by col2
    ,()         -- SumTotal grouped by col1, col2
)
```
The result would look like this:

![grouping-sets][grouping-sets]

An alternative to using `GROUPING SETS` is `ROLLUP`. `ROLLUP` does aggregations assuming there is a hierarchy:
```
SELECT col1
    ,col2
    ,SUM(col3) AS SumTotal
FROM dbo.SomeTable
GROUP BY
ROLLUP (col1, col2)
ORDER BY col1, col2
```

Using `CUBE` instead of `ROLLUP` gives us all potential combinations of groupings.

> Note: If you use many grouping sets, it becomes quite hard to identify which row belongs to which group result

You can use a helper function to make this task easier:
```
SELECT 
    GROUPING_ID(col1) as col1_group     -- 0/1, if this row is grouped
    ,GROUPING_ID(col2) as col2_group
    ,col1
    ,col2
    ,SUM(col3) as SumTotal
FROM dbo.SomeTable
GROUP BY CUBE(col1, col2)
ORDER BY col1, col2
```
Personally, I am not a huge fan of using these functions, because I feel the result sets can be hard to understand. I prefer to use WINDOW functions to give me different aggregation levels.

A rather nice way of using `ROLLUP` together with `CHOOSE` and `GROUPING_ID` is like so:
```
CHOOSE(1 + GROUPING_ID(col1) + GROUPING_ID(col_2), 
col1 + 'Subtotal', col2 + 'Subtotal', 'Total') as Level
```

### Pivoting
Pivoting data on the other hand is often very useful. Pivoting involves changing the format of your data from long to wide or wide to long:

![pivoting][pivoting]

The syntax for pivoting is:
```
SELECT
    Col1
    ,A1
    ,B2
    ,C3
FROM (
    SELECT Col1, Col2, col3 
    FROM dbo.SomeTable
) AS tmp
PIVOT (SUM(Col2) FOR Col3 IN([A1], [B2], [C3])) AS pvt
```
As you can see, we need to specify all columns that we want to receive in advance. If you want to do that dynamically, you have to look into dynamic SQL (or use R/Python:).

## Error handling

In SQL Server (not Azure SQL database) error messages are stored in `sys.messages` and we can add custom messages using `sp_addmessage`.

```
-- Check messages:
SELECT * 
FROM sys.messages
```

You can trow an error with the `THROW` command:
```
THROW 50001, 'Error', 0;
```
The error number needs to be greater than 50k. I can specify an arbitrary error message and a state. With user-defined errors the severity is always set to 16. 

We can also do try-catch using, you guessed it, a try-catch block:)
```
BEGIN TRY
    ...
END TRY
BEGIN CATCH
    ...
    PRINT 'Error message:'
    PRINT ERROR_MESSAGE()
    ...
END CATCH
```

## Transactions
Have you ever accidentally deleted or altered data? If you use Dropbox or Onedrive, you probably used the restore/rollback functionality to restore your data. Using transactions, you can define blocks that you wish to rollback in case you are not happy with the final result for any reason. A transaction is a group of tasks that must succeed or fail together. 

Individual data modifications are automatically treated as a transaction. 

The syntax is as follows:
```
BEGIN TRANSACTION       -- start transaction
    ...
COMMIT TRANSACTION      -- complete transaction
    ...
ROLLBACK TRANSACTION    -- rollback the transaction

```

## Reducing table sizes
If you started of with a database containing only tables in rowstore format, you can save lots of disk space by switching to a columnstore format.

However, SQL Server will not release the disk space until you tell it to.

Fortunately, this is really simple:

1. In Object Explorer go to the database you want to shrink
2. Right click the database and select `Tasks > Shrink > Files'
3. Reduce disk size in the dialog box


## Collaborating using Git
While most database admins and developers really like SQL Server Management Studio, it does not provide Git integration, meaning you need to fire up git in a console or use a source control tool such as Gitkraken. This is where VS Code or SQL Operations Studio come to the rescue:)

My preferred workflow is to use VS Code with the `mssql` extension to author my .sql files and put them in version control. I usually create a stored procedure based on the following template:
```
/*
Description of stored proc

Use CTRL+SHIFT+E to execute only selected block.

Run for debugging/testing:
EXEC dbo.myStoredProc
*/

ALTER PROCEDURE dbo.myStoredProc
AS
BEGIN
...
END
```
I make changes to the stored proc, send them to the database and debug it using `EXEC`. 

When I am satisfied with the results I add my stored procedure to our feature generation pipeline script.

I hope you found this post useful:) If you find any errors, please create an issue on Github.

[grouping-sets]: /img/grouping-sets.PNG "Results - grouping sets"
[pivoting]: /img/pivoting.PNG "Pivoting data"

