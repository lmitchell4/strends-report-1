# -*- coding: utf-8 -*-

"""
Created on Fri Dec 28 18:33:09 2018
script to read data files into memory as pandas dataframes and push 
to a postgresql db
@author: jsaracen
"""
#TODO: read all hardcoded file and sheet names from a file
import json
import pandas as pd
import pyodbc

from setup_paths import FILE_PATHS_PATH,TABLE_NAMES_PATH

def read_flow_index(filename):
    flow = pd.read_csv(filename)
    return flow
    
def read_emp_water_quality(filename):
    emp_wq = pd.read_excel(filename)
    return emp_wq

def read_json_to_dict(json_file):
    with open(json_file, "r") as f:
        json_dict = json.load(f)
    return json_dict


def write_table_names(fname, tablenames):
    with open(fname, 'w') as f:
        for item in tablenames:
            f.write("%s\n" % item)


def get_db_tables(PATH_TO_DB, TABLE_NAMES, SUFFIX='SKT'):        
    # connect to CDFW access database files
    #PATH_TO_DB = SLS_LS_PATH
#    FILE_PATHS_FILENAME = "file_paths.json" 
#    datafile_paths = read_json_to_dict(FILE_PATHS_FILENAME)
#    SLS_LS_PATH = datafile_paths.get("SLS_LS_PATH")
#    PATH_TO_DB=SLS_LS_PATH
#    #PATH_TO_DB =r"\data\FISH\SLS.mdb"
#    TABLE_NAME = "Catch"
    DRV = "Microsoft Access Driver (*.mdb, *.accdb)"
    PWD = "pw"
    SQL_DRIVERS = pyodbc.drivers()
    # connect to db
    if next((s for s in SQL_DRIVERS if DRV in s), None):
        CONXN = pyodbc.connect("DRIVER={};DBQ={};PWD={}".format(DRV, PATH_TO_DB, PWD))

        dataframes = []
        TABLE_NAMES_APPENDED =  [SUFFIX + '_' +  k for k in TABLE_NAMES]
        for TABLE_NAME in TABLE_NAMES:
            if " " in TABLE_NAME:
                TABLE_NAME = "[{}]".format(TABLE_NAME)
            SQL_QUERY = "SELECT * FROM {};".format(TABLE_NAME)  # catch query
            dataframes.append(pd.read_sql(SQL_QUERY, CONXN))
        CONXN.close()
        return dict(zip(TABLE_NAMES_APPENDED,dataframes))


def read_data_files(FILE_PATHS_FILENAME):
    print("Reading data files...")
    datafile_paths = read_json_to_dict(FILE_PATHS_FILENAME)
    # read paths to data files
    #WQ_WDL_PATH = datafile_paths.get("WQ_WDL_PATH")
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
    CBmatrix  = pd.read_excel(ZOOPLANKTON_CBMATRIX_PATH, sheet_name="CB CPUE Matrix 1972-2017") 
    # mysids counts from tow
    Mysidmatrix = pd.read_excel(ZOOPLANKTON_MYSID_PATH, sheet_name="Mysid CPUE Matrix 1972-2017")    
    Pumpmatrix = pd.read_excel(ZOOPLANKTON_PUMP_PATH, sheet_name="Pump CPUE Matrix 1972-2017")

    #FISH
    djfmp = pd.read_csv(DJFMP_PATH, low_memory=False)
    ybp_salmon = pd.read_csv(YBP_SALMON_PATH, low_memory=False)    
    ls_smelt = pd.read_excel(LS_SMELT_PATH, sheet_name="MWT Catch Matrix")  
    
    #TODO: read these table names from an external flat file
    SLS_LS_TABLENAMES = ["Catch", "20mm Stations", "AreaCode1", "Lengths",
                         "Meter Corrections", "Tow Info", "Water Info",
                         "Wt_factors"]
#    ls_sls_Catch = get_db_table(SLS_LS_PATH,"Catch" )
#    ls_sls_Twenty_mm_stations = get_db_table(SLS_LS_PATH,  "20mm Stations")
#    ls_sls_AreaCode1 = get_db_table(SLS_LS_PATH,"AreaCode1")
#    ls_sls_FishCodes = get_db_table(SLS_LS_PATH, "Lengths")
#    ls_sls_MeterCorrections = get_db_table(SLS_LS_PATH, "Meter Corrections")
#    ls_sls_TowInfo = get_db_table(SLS_LS_PATH, "Tow Info")
#    ls_sls_WaterInfo = get_db_table(SLS_LS_PATH, "Water Info")
#    ls_sls_Wt_factors = get_db_table(SLS_LS_PATH, "Wt_factors")
    SKT_DS_TABLENAMES = ["lktblStationsSKT", "tblCatch", "tblFishInfo",
                         "tblOrganismCodes", "tblReproductiveStages",
                         "tblSample", "tblSexLookUp"]
    
    SLS_LS_TABLES = get_db_tables(SLS_LS_PATH, SLS_LS_TABLENAMES, SUFFIX="SLS")
    SKT_DS_TABLES = get_db_tables(SKT_DS_PATH, SKT_DS_TABLENAMES, SUFFIX="SKT")
    
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
    #joing the dicts of datatables form the access databases to the out dict
    out_dict.update(SLS_LS_TABLES)
    out_dict.update(SKT_DS_TABLES)
    return out_dict

        
if __name__ == "__main__":
    # load in the datafile paths datafiles json file  
    
    data = read_data_files(FILE_PATHS_PATH)
    write_table_names(TABLE_NAMES_PATH,
                      data.keys()) # for querying data with ext hardware
