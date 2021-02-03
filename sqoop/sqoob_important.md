### Protecting Your Password
**Problem** <br>
Typing your password into the command-line interface is insecure. It can be easily retrieved from listing the operating system’s running processes.

Solution
You have two options besides specifying the password on the command line with the --password parameter. The first option is to use the parameter -P that will instruct Sqoop to read the password from standard input. Alternatively, you can save your password in a file and specify the path to this file with the parameter --password-file.

Here’s a Sqoop execution that will read the password from standard input:

    sqoop import \
      --connect jdbc:mysql://mysql.example.com/sqoop \
      --username sqoop \
      --table cities \
      -P
Here’s an example of reading the password from a file:

    sqoop import \
      --connect jdbc:mysql://mysql.example.com/sqoop \
      --username sqoop \
      --table cities \
      --password-file my-sqoop-password
Discussion
Let’s take a deeper look at each available method. The first method, using the parameter -P, will instruct Sqoop to prompt the user for the password before any other Sqoop action is taken. An example prompt is shown below:

sqoop import -P --connect ...
Enter password:
You can type any characters into the prompt and then press the Enter key once you are done. Sqoop will not echo any characters, preventing someone from reading the password on your screen. All entered characters will be loaded and used as the password (except for the final enter). This method is very secure, as the password is not stored anywhere and is loaded on every Sqoop execution directly from the user. The downside is that it can’t be easily automated with a script.

The second solution, using the parameter --password-file, will load the password from any specified file on your HDFS cluster. In order for this method to be secure, you need to store the file inside your home directory and set the file’s permissions to 400, so no one else can open the file and fetch the password. This method for securing your password can be easily automated with a script and is the recommended option if you need to securely automate your Sqoop workflow. You can use the following shell and Hadoop commands to create and secure your password file:


## Overriding Type Mapping
Problem<br>
The default type mapping that Sqoop provides between relational databases and Hadoop usually works well. You have use cases requiring you to override the mapping.

Solution
Use Sqoop’s ability to override default type mapping using the parameter --map-column-java. For example, to override the type of column id to Java type Long:

    sqoop import \
      --connect jdbc:mysql://mysql.example.com/sqoop \
      --username sqoop \
      --table cities \
      --map-column-java id=Long
Discussion
The parameter --map-column-java accepts a comma separated list where each item is a key-value pair separated by an equal sign. The exact column name is used as the key, and the target Java type is specified as the value. For example, if you need to change mapping in three columns c1, c2, and c3 to Float, String, and String, respectively, then your Sqoop command line would contain the following fragment:

sqoop import --map-column-java c1=Float,c2=String,c3=String ...

**ex**:
```bash
sqoop import 
--connect jdbc:mysql://localhost/retail_db --username root --password cloudera 
--table customers 
--target-dir /user/cloudera/new-customer_condition_columns_1 
--map-column-java customer_fname=String
```

## Importing All Your Tables
```bash
sqoop import-all-tables \
--connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera 
```
## If you need to import all but a few tables, you can use the parameter `--exclude-tables` that accepts a
```bash
sqoop import-all-tables \
--connect jdbc:mysql://localhost/retail_db \
--username root \
--password cloudera \
--exclude-tables cities,countries
```
