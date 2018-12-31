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

def read_flow_data(flow_csv_path):
        # IMPORT FLOW
    # FLOW INDEX DATA
    flow_path = os.path.join(os.pardir, r"data\FLOW")
    flowindex_fname = os.path.join(flow_path, 'dayflowCalculations2017.csv')
    flowindex = pd.read_csv(flowindex_fname)
    # import all flow data to date
    outflow_fname = os.path.join(flow_path, 'flow_1929-10-01_2017-09-30.csv')
    outflow = pd.read_csv(outflow_fname, index_col=[0])
    outflow.index = pd.to_datetime(outflow.index)
    

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


  ftp_zoo_dir = 'IEP_Zooplankton'
    cb_fname = '1972-2017CBMatrix.xlsx'
    # copepod counts from tows
    CBmatrix_fname = os.path.join(zoo_path, cb_fname)
    if not os.path.isfile(CBmatrix_fname):
        get_ftp_file(cdfw_ftp_addr, ftp_zoo_dir, cb_fname,
                     to_path=zoo_path)
    else:
        CBmatrix = pd.read_excel(CBmatrix_fname,
                                 sheet_name='CB CPUE Matrix 1972-2017')
    # mysids counts from tow
    my_fname = '1972-2017MysidMatrix.xlsx'
    mysid_fname = os.path.join(zoo_path, my_fname)
    if not os.path.isfile(mysid_fname):
        get_ftp_file(cdfw_ftp_addr, ftp_zoo_dir, my_fname,
                     to_path=zoo_path)
    else:
        Mysidmatrix = pd.read_excel(mysid_fname,
                                    sheet_name='Mysid CPUE Matrix 1972-2017')
    # mysids counts on the pump samples
    pump_fname = '1972-2017PumpMatrix.xlsx'
    Pumpmatrix_fname = os.path.join(zoo_path, pump_fname)
    if not os.path.isfile(Pumpmatrix_fname):
        get_ftp_file(cdfw_ftp_addr, ftp_zoo_dir, pump_fname,
                     to_path=zoo_path)
    else:
        Pumpmatrix = pd.read_excel(Pumpmatrix_fname,
                                   sheet_name='Pump CPUE Matrix 1972-2017')
    #PHYTOPLANKTON
    
    emp_phyto = pd.read_csv(emp_phyto_fname)
    
    djfmp_fname = os.path.join(fish_path, 'djfmp.csv')
    djfmp = pd.read_csv(djfmp_fname)
    ybp_salmon_fname = os.path.join(fish_path, 'ybp_salmon.csv')

    ybp_salmon = pd.read_csv(ybp_salmon_fname)