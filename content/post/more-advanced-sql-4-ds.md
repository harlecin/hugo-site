+++
date = "2018-05-05"
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

## Indices and columnstore

## Views & Table Variables

Views are simply named queries that we can interact with as if they were normal tables. We are 'viewing' through the view into the tables underneath.

Creating a view is a simple as:
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
Table variables should be only used on very small datasets and are only available during execution of the query (in contrast to temp tables).

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
Note that we did not put the parameter in parenthesis in order to pass it to the stored procedure. Replace `CREATE` with `ALTER` to change or update an existing stored procedure.

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

A rather nice way of using `ROLLUP` is together with `CHOOSE` and `GROUPING_ID` like so:
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

<CHECK!!!>

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

<enable read - Albert code here>

<sql server ram/cpu/disk limits>

[grouping-sets]: /img/grouping-sets.PNG "Results - grouping sets"
[pivoting]: /static/img/pivoting.PNG "Pivoting data"

### ToDos:
- Check pivot/unpivot
- Check Choose structure
