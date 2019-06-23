# Redshift

## CSV to AWS S3 and then to Redshift

The python script is given in this repository:
- Takes a CSV data file from redshift.data.
- Loads this into a MySQL database.
- Marshmallow (serializer/deserializer) is used to get the model data as list.
- The list is saved as a bytes I/O to S3.
- From S3 the data is copied to Redshift.

## Challenges

- [Five Queries](#Five-Queries)
- [Write Redshift Python Script](#Write-Redshift-Python-Script)

## Five Queries

### The Queries

The model is given below the five following queries that are built using MySQL instead of SQL.

(1) Write MySQL Query to list all the Sales for the state of California in the year 2018. List all the sales, meaning the complete row from sales.
```
SELECT Customer.CUST_ID, Customer.STATE, ORDERS.CUST_ID, ORDERS.SALES_DATE
FROM Customer
INNER JOIN ORDERS
ON Customer.CUST_ID = ORDERS.CUST_ID
WHERE Customer.STATE = 'CA' AND YEAR(ORDERS.SALES_DATE) = '2018';
```

(2) Write MySQL query to list Sales amount for each department in the year 2018 sorted by the sales amount. (Show all the department even if it did not make any sales).
```
SELECT Department.DEPARTMENT_NAME, SUM(ORDERS.ORDER_AMOUNT) AS total_sales
FROM ORDERS
INNER JOIN Salesman
ON ORDERS.SALESMAN_ID = Salesman.SALESMAN_ID
INNER JOIN Department
ON Salesman.DEPT_ID = Department.DEPT_ID
WHERE YEAR(ORDERS.SALES_DATE) = '2018'
GROUP BY Department.DEPARTMENT_NAME
ORDER BY total_sales;
```

(3) Write MySQL to list all the salesman who did not make any sales in 2018. If you also want total sales listed, remove the outer select, while leaving only the inner.
```
SELECT t1.SALESMAN_NAME from (SELECT SALESMAN.SALESMAN_NAME, SUM(ORDERS.ORDER_AMOUNT) AS total_sales
FROM ORDERS
INNER JOIN Salesman
ON Salesman.SALESMAN_ID = ORDERS.SALESMAN_ID
WHERE YEAR(ORDERS.SALES_DATE) = '2018'
GROUP BY Salesman.SALESMAN_NAME) as t1
WHERE total_sales = 0.00;
```

(4) Write MySQL to list Top 10 Salesman in the Year 2018 based on the sales. If you also want total sales listed, remove the outer select, while leaving only the inner.
```
SELECT t1.SALESMAN_NAME from (SELECT SALESMAN.SALESMAN_NAME, SUM(ORDERS.ORDER_AMOUNT) AS total_sales
FROM ORDERS
INNER JOIN Salesman
ON Salesman.SALESMAN_ID = ORDERS.SALESMAN_ID
WHERE YEAR(ORDERS.SALES_DATE) = '2018'
GROUP BY Salesman.SALESMAN_NAME
ORDER BY total_sales DESC LIMIT 10) as t1;
```

(5) Write MySQL to list Top 10 Customers in the Year 2018 based on the sales. If you also want total sales listed, remove the outer select, while leaving only the inner.
```
SELECT t1.CUST_NAME FROM (SELECT Customer.CUST_NAME, SUM(ORDERS.ORDER_AMOUNT) AS total_sales
FROM ORDERS
INNER JOIN Customer
ON CUSTOMER.CUST_ID = ORDERS.CUST_ID
WHERE YEAR(ORDERS.SALES_DATE) = '2018'
GROUP BY Customer.CUST_NAME
ORDER BY total_sales DESC LIMIT 10) AS t1;
```

### The MySQL Query Model

Here is the model for the queries given above.

```
CREATE TABLE `Department` (
    `DEPT_ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `DEPARTMENT_NAME` varchar(25) DEFAULT '',
    `Manager` varchar(25) DEFAULT '',
    PRIMARY KEY (`DEPT_ID`)
) AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Salesman` (
    `SALESMAN_ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `SALESMAN_NAME` varchar(25) DEFAULT '',
    `DEPT_ID` int(10) UNSIGNED NOT NULL,
    PRIMARY KEY (`SALESMAN_ID`),
    FOREIGN KEY (DEPT_ID) REFERENCES Department(DEPT_ID)
) AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Customer` (
    `CUST_ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `CUST_NAME` varchar(25) DEFAULT '',
    `ADDRESS` varchar(25) DEFAULT '',
    `CITY` varchar(25) DEFAULT '',
    `STATE` varchar(25) DEFAULT '',
    PRIMARY KEY (`CUST_ID`)
) AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Orders` (
    `ORDER_ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `SALES_DATE` DATETIME,
    `ORDER_AMOUNT` DECIMAL(5, 2) DEFAULT 0,
    `CUST_ID` int(10) UNSIGNED NOT NULL,
    `SALESMAN_ID` int(10) UNSIGNED NOT NULL,
    PRIMARY KEY (`ORDER_ID`)
) AUTO_INCREMENT=1 ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## Write Redshift Python Script

The python script is given in this repository:
- Takes a CSV data file from redshift.data.
- Loads this into a MySQL database.
- Marshmallow (serializer/deserializer) is used to get the model data as list.
- The list is saved as a bytes I/O to S3.
- From S3 the data is copied to Redshift.

### Tasks

(6) Import .csv file into TEST_MSR_SOURCE using Python Script
(7) Write a Python script that takes all data from TEST_MSR_SOURCE and inserts the data into TEST_MSR_TARGET

- Database type = Redshift
- Number of rows = 10
- Sequential key used for TEST_MSR_TARGET_ID
- Data transformations from varchar to (date, int, numeric, timestamp)

(8) Would your script change if the number of rows = 1,000,000? Why or why not?

### The Redshift Python Script Models

#### Local Database
```
CREATE TABLE TEST_MSR_SOURCE (
  rpt_grp_cd varchar(60) ,
  lctn_typ_cd varchar(10) ,
  clctn_prd_txt varchar(8) ,
  msr_cd varchar(20),
  clcltn_date varchar(10),
  grp_rate_nmrtr varchar(3),
  grp_rate_dnmntr varchar(5) ,
  file_name varchar(50),
  creat_ts varchar(50),
  creat_user_id varchar(30),
  submsn_cmplt_cd varchar(1))
```

#### Redshift Database
```
CREATE TABLE TEST_MSR_TARGET (
  TEST_MSR_TARGET_ID int4 NOT NULL
  rpt_grp_cd varchar(60),
  lctn_typ_cd varchar(10),
  clctn_prd_txt varchar(8),
  msr_cd varchar(20),
  clcltn_date date,
  grp_rate_nmrtr int4,
  grp_rate_dnmntr numeric(5),
  file_name varchar(50),
  finl_sw varchar(1),
  creat_ts timestamp NOT NULL,
  creat_user_id varchar(30) NOT NULL,
  submsn_cmplt_cd varchar(1))
```
