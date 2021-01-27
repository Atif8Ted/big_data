### Connection to sql
```bash
mysql -uroot -pcloudera -hlocalhost
```
### SQOOP Import
```bash

```
* once the import is done the files will be
copied to `hdfs dfs -ls /user/cloudera/customers`
  location
    
* ##### Specifying no of mappers
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers -m 2
```
* ##### By default if we dont specify output directory it will got to `/usr/cloudera/customers`
### Now lets pass the output directory as well.
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--warehouse-dir /user/cloudera/new-warehouse
```
>> the output will be stored in the parent directory `/user/cloudera/new-warehouse` with an additional
>  subfolder called customer `/user/cloudera/new-warehouse/customers`


### Suppose we directly want to import our data directly to the target-dir then we can use.
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new-customer
```
>> Now the files will be imported directly under `/user/cloudera/new-customer`

### Import sqoop will give error if the target directory already exists 
>> So we can use `--delete-target-dir` to overwrite existing data

```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new-customer \
--delete-target-dir
```
### By default the part files are generated in text file
### to set output formats use below command.
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new-customer_avro \
--as-avrodatafile
```
## Avro file  :
>> Avro file is like json <key:value>, but the difference is the data is stored in binary format.
`ex`:
```json
{"customer_id":{"int":3106},"customer_fname":{"string":"Samantha"},"customer_lname":{"string":"Smith"},"customer_email":{"string":"XXXXXXXXX"},"customer_password":{"string":"XXXXXXXXX"},"customer_street":{"string":"355 Cozy Square"},"customer_city":{"string":"Las Cruces"},"customer_state":{"string":"NM"},"customer_zipcode":{"string":"88005"}}
{"customer_id":{"int":3107},"customer_fname":{"string":"Tiffany"},"customer_lname":{"string":"Estes"},"customer_email":{"string":"XXXXXXXXX"},"customer_password":{"string":"XXXXXXXXX"},"customer_street":{"string":"5182 Cotton Heath"},"customer_city":{"string":"Caguas"},"customer_state":{"string":"PR"},"customer_zipcode":{"string":"00725"}}
{"customer_id":{"int":3108},"customer_fname":{"string":"Mary"},"customer_lname":{"string":"Smith"},"customer_email":{"string":"XXXXXXXXX"},"customer_password":{"string":"XXXXXXXXX"},"customer_street":{"string":"577 Rustic Nectar Row"},"customer_city":{"string":"Houston"},"customer_state":{"string":"TX"},"customer_zipcode":{"string":"77083"}}
{"customer_id":{"int":3109},"customer_fname":{"string":"Jack"},"customer_lname":{"string":"James"},"customer_email":{"string":"XXXXXXXXX"},"customer_password":{"string":"XXXXXXXXX"},"customer_street":{"string":"5876 Burning Mall "},"customer_city":{"string":"Fort Worth"},"customer_state":{"string":"TX"},"customer_zipcode":{"string":"76133"}}

```
>>  ` hdfs dfs -text /user/cloudera/new-customer_avro/part-m-00000.avro`
will help in visualing the content of avro file

### Output as parquet file

```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new_customer_parquet \
--as-parquetfile
```

### output as a sequence file.
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new_customer_sequence \
--as-sequencefile
```
### Sqoop import with compressions
* ##### Default is `gzip` format
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new_customer_compressed \
--compress
```
* #### cmopressing in snappy format
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new_customer_compressed_snappy \
--compress \
--compression-codec snappy
```
* #### cmopressing in deflate format
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new_customer_compressed_deflate \
--compress \
--compression-codec deflate
```
* #### cmopressing in bzip format
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new_customer_compressed_bzip \
--compress \
--compression-codec bzip2
```

* #### cmopressing in lz4 format
```bash
sqoop import --connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--table customers \
--target-dir /user/cloudera/new_customer_compressed_lz4 \
--compress \
--compression-codec lz4
```
### `NOTE` : lz4 compression is considered a good choice since ,
* it provides good compression.
* It is splittable.
* It is fast to compress and decompress.
