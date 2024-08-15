# SQLI fetcher for ctf chall
Making SQL injection payloads is pain in the ass, so let this code write the payload for you.

feel free to contribute ❤️

```
usage: sqli_fetcher.py [-h] [-m {tables,columns,data}] [-c COLUMN_COUNT] [-t TABLE] [-b {0,1}] [-k KEYSTRING] [-s SUBSTITUTION] [-d DBCONTEXT] [-u URL] [-l LIKE]  
                       [-mo {bool,time}]
                       payload

SQL Injection Fetcher

positional arguments:
  payload               Your SQL injection payload

options:
  -h, --help            show this help message and exit
  -m {tables,columns,data}, --method {tables,columns,data}
                        Method to use
  -c COLUMN_COUNT, --column_count COLUMN_COUNT
                        Number of columns to return
  -t TABLE, --table TABLE
                        Table to return
  -b {0,1}, --blind {0,1}
                        Blind mode (0 for no, 1 for yes)
  -k KEYSTRING, --keystring KEYSTRING
                        Keystring for the query
  -s SUBSTITUTION, --substitution SUBSTITUTION
                        Character substitution (comma-separated) format: {old},{new},{old2},{new2},etc...
  -d DBCONTEXT, --dbcontext DBCONTEXT
                        Database context (default mysql)
  -u URL, --url URL     URL for blind mode
  -l LIKE, --like LIKE  LIKE statement for blind mode
  -mo {bool,time}, --mode {bool,time}
                        Blind mode (bool or time)
```