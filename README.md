# Dorsa Database Module
## mysql version

[![N|Solid](https://dorsa-co.ir/wp-content/uploads/2022/04/Dorsa_Logo.png)](https://dorsa-co.ir)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This module used to connect mysql database with special functions that we want


## Features

- Create Schema
- Get name of all schemas
- Connect to the desired database
- Create/Delete table
- Add/Remove column
- Add/Update/Remove record

## Tech

This module used this Languages :

- [Python] 
- [MySql] 

## Installation


Install the dependencies and devDependencies and start the server.

```sh
cd Module_database
pip install -r requirements.txt
```

# Step1: Initialize the dataBase class with your MySQL database credentials:
In your script import Database and set your parms ( username , password , database name ) in your file and create an Object if your dont see Error while connecting your connection has been created
if you dont have database automatic create your schema
``` python
import Database

db = dataBase(username = 'YOUR_USERNAME', password = 'YOUR_PASSWORD', host = 'localhost', database_name = 'YOUR_SCHEMA')
```
# Step2: Create table and columns
You can use function create table to create it , or , just add column .
in two way table has been created .
All tables have id column .
``` python

db.create_table('users')   # you can dont create table
db.add_column(table_name='users',col_name='first_name',type=VARCHAR,len=80,Null=NOT_NULL)
db.add_column(table_name='users',col_name='last_name',type=VARCHAR,len=80,Null=NOT_NULL)
db.add_column(table_name='users',col_name='email',type=VARCHAR,len=80,Null=NOT_NULL)
```
# Step3: Add record
For add record you shold create tuple of your data and set in the function.
``` python
__YOUR_DATA__ = ('milad','moltaji','m.moltaji')
ret =db.add_record('users',data='__YOUR_DATA__')
```

## Step4 : Get data of table
To get the data of table, it is enough to give the desired table name to the function
``` python
content = db.get_all_content('users')
```

# Remove Record
To remove record set your table name , col name , and value
``` python
ret = db.remove_record(table_name='users',col_name='first_name',value='milad')
```




















