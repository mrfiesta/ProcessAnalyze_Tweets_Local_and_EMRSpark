#!/usr/bin/env python
#####Run and develoed in Ubuntu 18.04 and Python 3.6.7
import json
import os
#####Specify the folder where the file will be saved and where the credentials are
os.chdir('/PATH/ONYOURLOCAL/MACHINE/')
from config import config
import fileinput
import psycopg2

# from Leviathan import detect_language

#####Define the path previous to load the config library

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # Extract Database, this example is set for the Netherlands

        sql = "COPY (with t as (select FIELD1, FIELD2, FIELD_N from _NAME_OF_DATABASE_ where _COLUMN_LONGITUDE_ between 3.29 and 7.31 and _COLUMN_LATITUDE_ between 50.61 AND 53.69) select json_agg(t) from t) TO STDOUT"
        with open("/PATH/ONYOURLOCAL/MACHINE/completefile.txt", "w") as file:
            cur.copy_expert(sql, file)

        print('Extracting information from the database...')

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
     # adaptation of the postgrefile to a regular json format
    for line in fileinput.input(['completefile.txt'], inplace=True):
        print(line.replace('}, \\n {','}\r{'), end='')
    for line in fileinput.input(['completefile.txt'], inplace=True):
        print(line.replace('\\"',''), end='')
    for line in fileinput.input(['completefile.txt'], inplace=True):
        print(line.replace('\\',''), end='')
    for line in fileinput.input(['completefile.txt'], inplace=True):
        print(line.replace('[',''), end='')
    for line in fileinput.input(['completefile.txt'], inplace=True):
        print(line.replace(']',''), end='')

if __name__ == '__main__':
    connect()
