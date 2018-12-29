# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 18:33:09 2018
script to read data files into memory
@author: jsaracen
"""

import os
import os.path
import pandas as pd
import pyodbc
from fetch import fish_path, ls_smelt_fname

# TODO: create a multi-indexed dataframe based on date and station of smelt data
# ls_smelt.set_index(['Datetime', 'Station'], inplace=True)
# ls_smelt.iloc['DELSME', 'LONSME']

# connect to CDFW access database files
sls_db_fname = 'SLS.mdb'
MDB = os.path.join(fish_path, sls_db_fname)
DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'
PWD = 'pw'
SQL_DRIVERS = [pyodbc.drivers()[0],pyodbc.drivers()[1]]#,'{Microsoft Access Driver (*.mdb, *.accdb)}']
SQL_DRIVERS = pyodbc.drivers()
# connect to db
if next((s for s in SQL_DRIVERS if DRV in s), None):
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
    cur = con.cursor()
    
    # run a query and get the results
    SQL = 'SELECT * FROM Catch;'  # catch query
    rows = cur.execute(SQL).fetchall()
    cur.close()
    con.close()

# read in data
ls_smelt = pd.read_excel(ls_smelt_fname, sheet_name='MWT Catch Matrix')

ls_smelt['Datetime'] = pd.to_datetime(ls_smelt['Date'])
