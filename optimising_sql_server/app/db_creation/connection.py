import sqlite3
import configparser
from pandasql import sqldf
from optimising_sql_server.app.db_creation.logger import logger
from sqlalchemy import create_engine,MetaData,Table
import pandas as pd
import pyodbc


# config = configparser.ConfigParser()
# config.read('db.ini')
# print(config['DEFAULT']['databaseName'])

# databaseName = config['DEFAULT']['databaseName']
# username = config['mysql']['username']
# password = config['mysql']['password']
# server = config['mysql']['server']
# driver = config['mysql']['driver']

databaseName = 'new_db'
username = 'SA'
password = 'Passw0rd2018'
server = 'localhost,1433'
driver= 'ODBC Driver 17 for SQL Server'


CONNECTION_STRING = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+databaseName+';UID='+username+';PWD='+ password



class CreateDB:

    database = 'Data21Final'

    def __init__(self):
     
        
        self.db = pyodbc.connect(CONNECTION_STRING)# Create/Open a Connection to Microsoft's SQL Server
        self.c = self.db.cursor()# create cursor
        self.check_for_db()
        self.c.execute(f'USE {self.database}')
        self.c.commit()
        for i in self.c.execute('select DB_NAME() as [Current Database]'):
            logger.info(f'Connected to {i}\n')

    def check_for_db(self):
        dbs = [db[0] for db in self.c.execute('SELECT name FROM sys.databases')]
        logger.info(dbs)
        global databaseName
        if  self.database not in dbs:
            logger.info(f'Creating new database: {self.database}')
            self.db.autocommit = True
            self.c.execute(f'CREATE DATABASE {self.database}')
            self.c.execute(f'USE {self.database}')
            
            self.db.autocommit = False
            CONNECTION_STRING.replace(databaseName, self.database)
            logger.info(f'Changing connection string db to {self.database}')
        else: 
            databaseName = self.database



