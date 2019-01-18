# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 18:21:11 2018
script to fetch data from various repositories
@author: jsaracen
"""


from ftplib import FTP
import io
import json
import os
import os.path
import pandas as pd
import requests
import sys
import zipfile



def files_subdirs_in_root(path):
    """
    https://thomassileo.name/blog/2013/12/12/tracking-changes-in-directories-with-python/
    """
    files = []
    subdirs = []
    for root, dirs, filenames in os.walk(path):
        for subdir in dirs:
            subdirs.append(os.path.relpath(os.path.join(root, subdir), path))
    
        for f in filenames:
            files.append(os.path.relpath(os.path.join(root, f), path))
    return files, subdirs


def read_json_to_dict(json_file):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)
    return json_dict

def write_dict_to_json(sample_dict, json_file):
    with open(json_file, 'w') as fp:
        json.dump(sample_dict, fp)
    fp.close()
    return 


def get_ftp_file(addr, ftp_path, fname, to_path="", verbose=False):
    """ Function to grab a file, fname, from an ftp specified by addr
    at the given path and put in the local directory"""
    ftp = FTP(addr)
    ftp.login()
    if verbose:
        print("Welcome: ", ftp.getwelcome())
        ftp.retrlines("LIST")
    ftp.cwd(ftp_path)
    local_filename = os.path.join(to_path,  fname)
    filedata = open(local_filename, "wb")
    ftp.retrbinary("RETR " + fname, filedata.write)
    if verbose:
        print("Retrieving file:", fname)
    filedata.close()
    ftp.quit()
    return

def get_zooplankton(CDFW_FTP_ADDR, ftp_zooplankton_dir, ZOO_DIR, filenames):
    """ Funtion to pull ZOOPLANKTON workbooks from CDFW's FTP site"""
    
    cb_fname = filenames.get('ZOOPLANKTON_CBMATRIX_FILENAME',
                             "1972-2017CBMatrix.xlsx")
    # copepod counts from tows
    CBmatrix_fname = os.path.join(ZOO_DIR, cb_fname)
    if not os.path.isfile(CBmatrix_fname):
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, cb_fname,
                     to_path=ZOO_DIR)
    # mysids counts from tow
    my_fname = filenames.get('ZOOPLANKTON_MYSID_FILENAME',
                             "1972-2017MysidMatrix.xlsx")
    mysid_fname = os.path.join(ZOO_DIR, my_fname)
    if not os.path.isfile(mysid_fname):
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, my_fname,
                     to_path=ZOO_DIR)
    # mysids counts on the pump samples
    pump_fname = filenames.get('ZOOPLANKTON_PUMP_FILENAME',
                               "1972-2017PumpMatrix.xlsx")
    Pumpmatrix_fname = os.path.join(ZOO_DIR, pump_fname)
    if not os.path.isfile(Pumpmatrix_fname):
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, pump_fname,
                     to_path=ZOO_DIR)


def extractzip(loc, outloc):
        """
        using the zipfile tool extract here .
        This function is valid if the file type is zip only
        from Reezoo Bose (stackoverflow)
       """
        with zipfile.ZipFile(loc, "r") as zip_ref:
            print("Unpacking",loc, "to", outloc, "...")
            # iterate over zip info list.
            for item in zip_ref.infolist():
                zip_ref.extract(item, outloc)

            zip_ref.close()
            return  # zip_files

#TODO: Add try/except clauses
def fetch_data_files():
        ### SETUP DATA SOURCE LOCATIONS, DIRECTORIES, PATHS###
    # get the root directory of this script to set relative paths
    print("Fetching data...")
    ROOT_DIR = os.pardir # root directory
    DATA_DIR = r"data" #path to  data directory
    FISH_DIR = os.path.join(ROOT_DIR, DATA_DIR, "FISH")
    ZOO_DIR = os.path.join(ROOT_DIR, DATA_DIR, "ZOO")
    FLOW_DIR = os.path.join(ROOT_DIR, DATA_DIR, "FLOW")
    WQ_DIR =  os.path.join(ROOT_DIR, DATA_DIR, "WQ") #must manually download WQ datasets
    
    FTP_ZOO_DIR = "IEP_Zooplankton" # the zooplankton drectory name on the cdfw ftp 

    data_portal_urls_file = "data_portal_urls.json"    
    data_portal_urls = read_json_to_dict(data_portal_urls_file)
    CDFW_FTP_ADDR = data_portal_urls.get("CDFW_FTP_ADDR", "ftp.dfg.ca.gov")

    data_filenames_file = "data_filenames.json"    
    data_filenames = read_json_to_dict(data_filenames_file)
    
    #  FILE_PATHS_FILENAME = "file_paths.json" 

    FLOW_INDEX_FILENAME = data_filenames.get('FLOW_INDEX_FILENAME')
    FLOW_INDEX_PATH = os.path.join(FLOW_DIR, FLOW_INDEX_FILENAME)
    
    WQ_LAB_FILENAME = data_filenames.get('WQ_LAB_FILENAME')
    WQ_LAB_PATH = os.path.join(WQ_DIR, WQ_LAB_FILENAME)
    
    WQ_FIELD_FILENAME = data_filenames.get('WQ_FIELD_FILENAME')
    WQ_FIELD_PATH = os.path.join(WQ_DIR,  WQ_FIELD_FILENAME)
    
    WDL_WQ = data_filenames.get('WDL_WQ')
    WDL_WQ_PATH= os.path.join(WQ_DIR,  WDL_WQ)
    
    ZOOPLANKTON_CBMATRIX_PATH = os.path.join(ZOO_DIR, data_filenames.get('ZOOPLANKTON_CBMATRIX_FILENAME'))
    ZOOPLANKTON_MYSID_PATH = os.path.join(ZOO_DIR, data_filenames.get('ZOOPLANKTON_MYSID_FILENAME'))
    ZOOPLANKTON_PUMP_PATH = os.path.join(ZOO_DIR, data_filenames.get('ZOOPLANKTON_PUMP_FILENAME'))

    if not os.path.isdir(ZOO_DIR):
        os.mkdir(ZOO_DIR)
    get_zooplankton(CDFW_FTP_ADDR, FTP_ZOO_DIR, ZOO_DIR, data_filenames) 

    # IMPORT EMP PHYTOPLANKTON DATA
    PHYTO_DIR= os.path.join(ROOT_DIR, DATA_DIR, "PHYTO")
    if not os.path.isdir(PHYTO_DIR):
        os.mkdir(PHYTO_DIR)
    EMP_PHYTOPLANKTON_FILENAME = data_filenames.get("EMP_PHYTOPLANKTON_FILENAME",
                                                    "emp_phytoplankton.csv")
    EMP_PHYTO_PATH = os.path.join(PHYTO_DIR, EMP_PHYTOPLANKTON_FILENAME)
    EMP_PHYTOPLANKTON_URL = data_portal_urls.get("EMP_PHYTOPLANKTON_URL")
    if not os.path.isfile(EMP_PHYTO_PATH):        
        emp_phyto = pd.read_csv(EMP_PHYTOPLANKTON_URL)
        emp_phyto.to_csv(EMP_PHYTO_PATH, index=False)
    # IMPORT FISH DATA
    if not os.path.isdir(FISH_DIR):
        os.mkdir(FISH_DIR) 
    # Retrieve data from the EDI data repos
    # YOLO BYP SALMON FISH
    YBP_SALMON_FILENAME = data_filenames.get("YBP_SALMON_FILENAME",
                                             "ybp_salmon.csv") 
    YBP_SALMON_PATH = os.path.join(FISH_DIR, YBP_SALMON_FILENAME)
    YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL = data_portal_urls.get("YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL")
    if not os.path.isfile(YBP_SALMON_PATH):
        ybp_edi = requests.get(YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL).content
        ybp_salmon = pd.read_csv(io.StringIO(ybp_edi.decode("utf-8")))
        # save the file locally
        ybp_salmon.to_csv(YBP_SALMON_PATH, index=False)
        
    # USFWS Delta Juvenile Fish Monitoring Program
    DELTA_JUVENILE_FISH_MONITORING_PROGRAM_FILENAME = data_filenames.get("DELTA_JUVENILE_FISH_MONITORING_PROGRAM_FILENAME", "djfmp.csv")
    DJFMP_PATH = os.path.join(FISH_DIR, DELTA_JUVENILE_FISH_MONITORING_PROGRAM_FILENAME)
    DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL = data_portal_urls.get("DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL")

    if not os.path.isfile(DJFMP_PATH):
        djfmps_edi = requests.get(DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL).content
        djfmp = pd.read_csv(io.StringIO(djfmps_edi.decode("utf-8")))
        # save the file locally
        djfmp.to_csv(DJFMP_PATH, index=False)

    # move files from ftp to local space
    # TODO: ONLY COPY FILES IF AND ONLY IF THEY ARE UPDATED)
    # Smelt Larva Survey (CDFW): Longfin Smelt
    FTP_DS_DIR = "Delta Smelt"    
    SLS_DS_FILENAME = data_filenames.get("SLS_FILENAME", "SLS.mdb")
    SLS_DS_PATH = os.path.join(FISH_DIR, SLS_DS_FILENAME)
    
    if not os.path.isfile(SLS_DS_PATH):
        get_ftp_file(CDFW_FTP_ADDR, FTP_DS_DIR, SLS_DS_FILENAME,
                     to_path=FISH_DIR)
    
    # Spring Kodiak
    # Careful and be prepared to wait bc SKT is a large file (~400 MB)!
    SKT_FILENAME = data_filenames.get("SKT_FILENAME", "SKT.mdb")    
    SKT_LS_PATH = os.path.join(FISH_DIR, SKT_FILENAME)
    
    if not os.path.isfile(SKT_LS_PATH):
        get_ftp_file(CDFW_FTP_ADDR, FTP_DS_DIR, SKT_FILENAME,
                     to_path=FISH_DIR)
    
    # Bay Study (CDFW): Longfin Smelt
    #FETCH THE DATA
    LS_SMELT_FILENAME_ZIP = data_portal_urls.get("LS_SMELT_FILENAME_ZIP",
                                                 "Bay Study_FishCatchMatrices_1980-2017.zip")
    LS_ZIP_FILE_PATH = os.path.join(FISH_DIR, LS_SMELT_FILENAME_ZIP)
    FTP_LS_DIR = "BayStudy/CatchMatrices"
    if not os.path.isfile(LS_ZIP_FILE_PATH):        
        get_ftp_file(CDFW_FTP_ADDR, FTP_LS_DIR,
                     LS_SMELT_FILENAME_ZIP,
                     to_path=FISH_DIR)
    #UNZIP THE DATA
    BAYSTUDY_DIR = "BayStudy"
    LS_SMELT_DIR = os.path.join(FISH_DIR, BAYSTUDY_DIR)
    if not os.path.isdir(LS_SMELT_DIR):
        os.mkdir(LS_SMELT_DIR)
    LS_SMELT_FILENAME = data_portal_urls.get("LS_SMELT_FILENAME",
                                             "Bay Study_MWT_1980-2017_FishMatrix.xlsx")
    LS_SMELT_PATH = os.path.join(LS_SMELT_DIR, LS_SMELT_FILENAME)
                     
    if not os.path.isfile(LS_SMELT_PATH):
        # unpack zip files if necessary
        zip_ref = zipfile.ZipFile(LS_SMELT_FILENAME_ZIP, "r")
        zip_ref.extractall(path=LS_SMELT_PATH)
        zip_ref.close()
    
    
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

def main():
    """main entry point for the script"""
    pass

if __name__ == "__main__":
    
    sys.exit(main())