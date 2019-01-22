# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 18:33:09 2018
script to read data files into memory as pandas dataframes and push 
to a postgresql db
@author: jsaracen
"""
import json
import os
import os.path
import pandas as pd
import pyodbc


# TODO: create a multi-indexed dataframe based on date and station of smelt data
# ls_smelt.set_index(['Datetime', 'Station'], inplace=True)
# ls_smelt.iloc['DELSME', 'LONSME']

def read_flow_index(filename):
    flow = pd.read_csv(filename)
    return flow
    
def read_emp_water_quality(filename):
    #path  = os.path.join(os.pardir, r"data\WQ")
    #fname = os.path.join(path, '')
    #filename = os.path.join(path, fname)
    emp_wq = pd.read_excel(filename,)
    return emp_wq

def read_json_to_dict(json_file):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)
    return json_dict

def query_access_db(PATH_TO_DB, SQL_QUERY):        
    # connect to CDFW access database files
    #PATH_TO_DB = SLS_LS_PATH
    DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'
    PWD = 'pw'
    SQL_DRIVERS = pyodbc.drivers()
    # connect to db
    if next((s for s in SQL_DRIVERS if DRV in s), None):
        con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, PATH_TO_DB, PWD))
        cur = con.cursor()        
        # run a query and get the results
        #SQL_QUERY = 'SELECT * FROM Catch;'  # catch query
        rows = cur.execute(SQL_QUERY).fetchall()
        cur.close()
        con.close()
    return rows

def read_data_files(FILE_PATHS_FILENAME):
    print("Reading data files....")
    datafile_paths = read_json_to_dict(FILE_PATHS_FILENAME)
    # read paths to data files
    WQ_WDL_PATH = datafile_paths.get("WQ_WDL_PATH")     
    SKT_DS_PATH = datafile_paths.get("SKT_DS_PATH")
    SLS_LS_PATH = datafile_paths.get("SLS_LS_PATH")
    FLOW_INDEX_PATH = datafile_paths.get("FLOW_INDEX_PATH")    
    YBP_SALMON_PATH = datafile_paths.get("YBP_SALMON_PATH")
    DJFMP_PATH = datafile_paths.get("DJFMP_PATH")
    LS_SMELT_PATH = datafile_paths.get("LS_SMELT_PATH")#this reads the xlsx not the .mdb
    EMP_PHYTO_PATH = datafile_paths.get("EMP_PHYTO_PATH")
    FLOW_INDEX_PATH = datafile_paths.get("FLOW_INDEX_PATH")
    WQ_FIELD_PATH = datafile_paths.get("WQ_FIELD_PATH")
    WQ_LAB_PATH = datafile_paths.get("WQ_LAB_PATH")
    ZOOPLANKTON_MYSID_PATH = datafile_paths.get("ZOOPLANKTON_MYSID_PATH")
    ZOOPLANKTON_CBMATRIX_PATH = datafile_paths.get("ZOOPLANKTON_CBMATRIX_PATH")
    ZOOPLANKTON_PUMP_PATH = datafile_paths.get("ZOOPLANKTON_PUMP_PATH")
    
    # read data from files into pandas dataframes
    #Flow
    flow_index = read_flow_index(FLOW_INDEX_PATH)
    #WQ
    emp_wq_lab = read_emp_water_quality(WQ_LAB_PATH)
    emp_wq_field = read_emp_water_quality(WQ_FIELD_PATH)
    #wdl_wq_lab = pd.read_csv(WQ_WDL_PATH)    
    #PHYTOPLANKTON
    emp_phyto = pd.read_csv(EMP_PHYTO_PATH)      
    #ZOOPLANKTON
    #copepod counts from tows
    CBmatrix  = pd.read_excel(ZOOPLANKTON_CBMATRIX_PATH, sheet_name='CB CPUE Matrix 1972-2017')
    # mysids counts from tow
    Mysidmatrix = pd.read_excel(ZOOPLANKTON_MYSID_PATH, sheet_name='Mysid CPUE Matrix 1972-2017')    
    Pumpmatrix = pd.read_excel(ZOOPLANKTON_PUMP_PATH, sheet_name='Pump CPUE Matrix 1972-2017')

    #FISH
    djfmp = pd.read_csv(DJFMP_PATH, low_memory=False)
    ybp_salmon = pd.read_csv(YBP_SALMON_PATH, low_memory=False)
    ls_smelt = pd.read_excel(LS_SMELT_PATH, sheet_name='MWT Catch Matrix')
    
    out_dict = {
    "flow_index":flow_index, 
    "emp_wq_lab":emp_wq_lab,
    "emp_wq_field":emp_wq_field,
    "emp_phyto":emp_phyto, 
    "CBmatrix":CBmatrix, 
    "Mysidmatrix":Mysidmatrix,
    "Pumpmatrix":Pumpmatrix, 
    "djfmp":djfmp,
    "ybp_salmon":ybp_salmon, 
    "ls_smelt":ls_smelt
    }
    return out_dict

if __name__ == "__main__":
    # load in the datafile paths datafilesjson file
    FILE_PATHS_FILENAME = "file_paths.json" 
  
    data = read_data_files(FILE_PATHS_FILENAME)
 
 
    
