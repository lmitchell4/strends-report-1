# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 17:31:38 2019
script to setup directory paths and files
@author: jsaracen
INPUT:
"""

import json
import os

def read_json_to_dict(json_file):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)
    return json_dict

def write_dict_to_json(sample_dict, json_file):
    with open(json_file, 'w') as fp:
        json.dump(sample_dict, fp)
    fp.close()
    return 

data_portal_urls_file = "data_portal_urls.json"    
data_portal_urls = read_json_to_dict(data_portal_urls_file)
data_filenames_file = "data_filenames.json"    
data_filenames = read_json_to_dict(data_filenames_file)

#setup directories
ROOT_DIR = os.pardir # root directory
DATA_DIR = r"data" #path to  data directory
FISH_DIR = os.path.join(ROOT_DIR, DATA_DIR, "FISH")
ZOO_DIR = os.path.join(ROOT_DIR, DATA_DIR, "ZOO")
FLOW_DIR = os.path.join(ROOT_DIR, DATA_DIR, "FLOW")
WQ_DIR =  os.path.join(ROOT_DIR, DATA_DIR, "WQ") #must manually download WQ datasets
FTP_ZOO_DIR = "IEP_Zooplankton" # the zooplankton drectory name on the cdfw ftp 
CDFW_FTP_ADDR = data_portal_urls.get("CDFW_FTP_ADDR", "ftp.dfg.ca.gov")
FTP_DS_DIR = "Delta Smelt"  
    #UNZIP THE DATA
BAYSTUDY_DIR = "BayStudy"    
FTP_LS_DIR = "BayStudy/CatchMatrices"
LS_SMELT_DIR = os.path.join(FISH_DIR, BAYSTUDY_DIR)
# IMPORT EMP PHYTOPLANKTON DATA
PHYTO_DIR = os.path.join(ROOT_DIR, DATA_DIR, "PHYTO")
if not os.path.isdir(PHYTO_DIR):
    os.mkdir(PHYTO_DIR)

if not os.path.isdir(ZOO_DIR):
    os.mkdir(ZOO_DIR)
    
if not os.path.isdir(FISH_DIR):
    os.mkdir(FISH_DIR) 

if not os.path.isdir(LS_SMELT_DIR):
    os.mkdir(LS_SMELT_DIR)    
    
    
    
#read in the filenames and paths and set abs paths to files
FLOW_INDEX_FILENAME = data_filenames.get('FLOW_INDEX_FILENAME')
FLOW_INDEX_PATH = os.path.join(FLOW_DIR, FLOW_INDEX_FILENAME)

WQ_LAB_FILENAME = data_filenames.get('WQ_LAB_FILENAME')
WQ_LAB_PATH = os.path.join(WQ_DIR, WQ_LAB_FILENAME)

WQ_FIELD_FILENAME = data_filenames.get('WQ_FIELD_FILENAME')
WQ_FIELD_PATH = os.path.join(WQ_DIR,  WQ_FIELD_FILENAME)

WDL_WQ = data_filenames.get('WDL_WQ')
WDL_WQ_PATH= os.path.join(WQ_DIR,  WDL_WQ)

ZOOPLANKTON_CBMATRIX_FILENAME = data_filenames.get('ZOOPLANKTON_CBMATRIX_FILENAME')
ZOOPLANKTON_MYSID_FILENAME = data_filenames.get('ZOOPLANKTON_MYSID_FILENAME')
ZOOPLANKTON_PUMP_FILENAME = data_filenames.get('ZOOPLANKTON_PUMP_FILENAME')

ZOOPLANKTON_CBMATRIX_PATH = os.path.join(ZOO_DIR, data_filenames.get('ZOOPLANKTON_CBMATRIX_FILENAME'))
ZOOPLANKTON_MYSID_PATH = os.path.join(ZOO_DIR, data_filenames.get('ZOOPLANKTON_MYSID_FILENAME'))
ZOOPLANKTON_PUMP_PATH = os.path.join(ZOO_DIR, data_filenames.get('ZOOPLANKTON_PUMP_FILENAME'))
    
EMP_PHYTOPLANKTON_FILENAME = data_filenames.get("EMP_PHYTOPLANKTON_FILENAME",
                                                "emp_phytoplankton.csv")
EMP_PHYTO_PATH = os.path.join(PHYTO_DIR, EMP_PHYTOPLANKTON_FILENAME)
EMP_PHYTOPLANKTON_URL = data_portal_urls.get("EMP_PHYTOPLANKTON_URL")

YBP_SALMON_FILENAME = data_filenames.get("YBP_SALMON_FILENAME",
                                         "ybp_salmon.csv") 
YBP_SALMON_PATH = os.path.join(FISH_DIR, YBP_SALMON_FILENAME)
YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL = data_portal_urls.get("YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL")

DELTA_JUVENILE_FISH_MONITORING_PROGRAM_FILENAME = data_filenames.get("DELTA_JUVENILE_FISH_MONITORING_PROGRAM_FILENAME", "djfmp.csv")
DJFMP_PATH = os.path.join(FISH_DIR, DELTA_JUVENILE_FISH_MONITORING_PROGRAM_FILENAME)

DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL = data_portal_urls.get("DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL")


SLS_FILENAME = data_filenames.get("SLS_FILENAME", "SLS.mdb")
SLS_DS_PATH = os.path.join(FISH_DIR, SLS_FILENAME)

LS_SMELT_FILENAME_ZIP = data_portal_urls.get("LS_SMELT_FILENAME_ZIP",
                                             "Bay Study_FishCatchMatrices_1980-2017.zip")
LS_ZIP_FILE_PATH = os.path.join(FISH_DIR, LS_SMELT_FILENAME_ZIP)

LS_SMELT_FILENAME = data_portal_urls.get("LS_SMELT_FILENAME",
                                             "Bay Study_MWT_1980-2017_FishMatrix.xlsx")
LS_SMELT_PATH = os.path.join(LS_SMELT_DIR, LS_SMELT_FILENAME)
    
SKT_FILENAME = data_filenames.get("SKT_FILENAME", "SKT.mdb")    
SKT_LS_PATH = os.path.join(FISH_DIR, SKT_FILENAME)



FILE_PATHS_FILENAME = "file_paths.json" 
datafile_paths = {
                  "LS_SMELT_PATH":LS_SMELT_PATH,
                  "YBP_SALMON_PATH":YBP_SALMON_PATH,
                  "SKT_LS_PATH":SKT_LS_PATH,  
                  "SLS_DS_PATH":SLS_DS_PATH,
                  "DJFMP_PATH":DJFMP_PATH,
                  "EMP_PHYTO_PATH":EMP_PHYTO_PATH,
                  "LS_ZIP_FILE_PATH":LS_ZIP_FILE_PATH,
                  "FLOW_INDEX_PATH":FLOW_INDEX_PATH,
                  "WQ_FIELD_PATH":WQ_FIELD_PATH,
                  "WQ_LAB_PATH":WQ_LAB_PATH,
                  "WDL_WQ_PATH":WDL_WQ_PATH,
                  "ZOOPLANKTON_MYSID_PATH":ZOOPLANKTON_MYSID_PATH,
                  "ZOOPLANKTON_CBMATRIX_PATH":ZOOPLANKTON_CBMATRIX_PATH,
                  "ZOOPLANKTON_PUMP_PATH":ZOOPLANKTON_PUMP_PATH,
                  }

write_dict_to_json(datafile_paths, FILE_PATHS_FILENAME)