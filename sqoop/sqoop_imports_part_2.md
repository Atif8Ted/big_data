## Conditional Imports 

* ### Where clause

```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new-customer_condition \
--where "customer_fname='Mary'"
```
* ### with selected columns
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new-customer_condition_columns \
--columns "customer_fname,customer_lname,customer_city"
```
* ### **`query`** option 
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--target-dir /user/cloudera/new-customer_condition_query \
--query "select * from customers where customer_id>100 AND \$CONDITIONS" \
--split-by customer_id
```
* ### **`split-by`** clause
>> `split-by` clause is used to split file based on the column among the mappers.
>>> if no split-by clause is used , byt default the split is done on primary key of a table.
> 

### Prob-1  : fetch all orders from the orders table in mysql where order_status is complete
 ```bash 
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table orders \
--target-dir /user/cloudera/order_table_prob_2 \
--where "order_status='COMPLETE'" \
--compress \
--compression-codec snappy \
--as-parquetfile \
--null-string "NA" \
--null-non-string -1
```