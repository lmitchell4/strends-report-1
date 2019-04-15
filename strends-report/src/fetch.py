# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 18:21:11 2018
script to fetch data from various repositories
@author: jsaracen
"""


from ftplib import FTP
import io
import os
from pathlib import Path
import pandas as pd
import requests
import sys
import zipfile

#from setup_paths import * #LS_SMELT_PATH, YBP_SALMON_PATH SKT_LS_PATH', 'SLS_DS_PATH', 'DJFMP_PATH', 'EMP_PHYTO_PATH', 'LS_ZIP_FILE_PATH', 'FLOW_INDEX_PATH', 'WQ_FIELD_PATH', 'WQ_LAB_PATH', 'WDL_WQ_PATH', 'ZOOPLANKTON_MYSID_PATH', 'ZOOPLANKTON_CBMATRIX_PATH', 'ZOOPLANKTON_PUMP_PATH'
#from setup_paths import FLOW_INDEX_FILENAME,EMP_PHYTOPLANKTON_FILENAME,ZOOPLANKTON_MYSID_FILENAME,ZOOPLANKTON_PUMP_FILENAME,ZOOPLANKTON_CBMATRIX_FILENAME
#from setup_paths import LS_SMELT_FILENAME, YBP_SALMON_FILENAME,DELTA_JUVENILE_FISH_MONITORING_PROGRAM_FILENAME
#from setup_paths import WQ_LAB_FILENAME,WQ_FIELD_FILENAME,WDL_WQ
from setup_paths import LS_SMELT_FILENAME_ZIP, SLS_FILENAME,SKT_FILENAME
from setup_paths import EMP_PHYTO_PATH,YBP_SALMON_PATH, DJFMP_PATH,SKT_DS_PATH,LS_SMELT_PATH,LS_ZIP_FILE_PATH,SLS_LS_PATH
from setup_paths import CDFW_FTP_ADDR, FTP_ZOO_DIR, ZOO_DIR,FISH_DIR,FTP_LS_DIR,FTP_DS_DIR
from setup_paths import DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL,EMP_PHYTOPLANKTON_URL,YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL
from setup_paths import data_filenames


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
    fileconfig = Path(CBmatrix_fname)
    if not fileconfig.is_file():
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, cb_fname,
                     to_path=ZOO_DIR)
    # mysids counts from tow
    my_fname = filenames.get('ZOOPLANKTON_MYSID_FILENAME',
                             "1972-2017MysidMatrix.xlsx")
    mysid_fname = os.path.join(ZOO_DIR, my_fname)
    fileconfig = Path(mysid_fname)
    if not fileconfig.is_file():
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, my_fname,
                     to_path=ZOO_DIR)
    # mysids counts on the pump samples
    pump_fname = filenames.get('ZOOPLANKTON_PUMP_FILENAME',
                               "1972-2017PumpMatrix.xlsx")
    Pumpmatrix_fname = os.path.join(ZOO_DIR, pump_fname)
    fileconfig = Path(Pumpmatrix_fname)
    if not fileconfig.is_file():
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


#TODO: Add try/except clauses for each data fetching routines
#TODO: Only fetch the data if local copy is out of date with remote copy
def fetch_data_files():
        ### SETUP DATA SOURCE LOCATIONS, DIRECTORIES, PATHS###
    # get the root directory of this script to set relative paths
    print("Fetching data...")
    
    get_zooplankton(CDFW_FTP_ADDR, FTP_ZOO_DIR, ZOO_DIR, data_filenames) 

    if not Path(EMP_PHYTO_PATH).is_file():        
        emp_phyto = pd.read_csv(EMP_PHYTOPLANKTON_URL)
        emp_phyto.to_csv(EMP_PHYTO_PATH, index=False)
    # IMPORT FISH DATA
    # Retrieve data from the EDI data repos
    # YOLO BYP SALMON FISH
    fileconfig = Path(YBP_SALMON_PATH)
    if not fileconfig.is_file():
        ybp_edi = requests.get(YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL).content
        ybp_salmon = pd.read_csv(io.StringIO(ybp_edi.decode("utf-8")))
        # save the file locally
        ybp_salmon.to_csv(YBP_SALMON_PATH, index=False)
        
    # USFWS Delta Juvenile Fish Monitoring Program
    fileconfig = Path(DJFMP_PATH)
    if not fileconfig.is_file():
        djfmps_edi = requests.get(DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL).content
        djfmp = pd.read_csv(io.StringIO(djfmps_edi.decode("utf-8")))
        # save the file locally
        djfmp.to_csv(DJFMP_PATH, index=False)

    # move files from ftp to local space
    # TODO: ONLY COPY FILES IF AND ONLY IF THEY ARE UPDATED)
    # Smelt Larva Survey (CDFW): Longfin Smelt
    fileconfig = Path(SLS_LS_PATH)
    if not fileconfig.is_file():
        get_ftp_file(CDFW_FTP_ADDR, FTP_DS_DIR, SLS_FILENAME,
                     to_path=FISH_DIR)
    # Spring Kodiak
    # Careful and be prepared to wait bc SKT is a large file (~400 MB)!
    fileconfig = Path(SKT_DS_PATH)
    if not fileconfig.is_file():
        get_ftp_file(CDFW_FTP_ADDR, FTP_DS_DIR, SKT_FILENAME,
                     to_path=FISH_DIR)
    # Bay Study (CDFW): Longfin Smelt
    #FETCH THE DATA
    fileconfig =  Path(LS_ZIP_FILE_PATH)
    if not fileconfig.is_file():        
        get_ftp_file(CDFW_FTP_ADDR, FTP_LS_DIR,
                     LS_SMELT_FILENAME_ZIP,
                     to_path=FISH_DIR)
    fileconfig = Path(LS_SMELT_PATH)             
    if not fileconfig.is_file():
        # unpack zip files if necessary
        zip_ref = zipfile.ZipFile(LS_SMELT_FILENAME_ZIP, "r")
        zip_ref.extractall(path=LS_SMELT_PATH)
        zip_ref.close()


def main():
    """main entry point for the script"""
    fetch_data_files()
    return

if __name__ == "__main__":
    
    sys.exit(main())