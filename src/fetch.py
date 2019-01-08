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
import zipfile


def get_urls_from_json_file(urls_file):
    with open(urls_file) as f:
        urls = json.load(f)
    return urls


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

def get_zooplankton(CDFW_FTP_ADDR, ftp_zooplankton_dir, ZOO_DIR):
    """ Funtion to pull ZOOPLANKTON workbooks from CDFW's FTP site"""
    cb_fname = "1972-2017CBMatrix.xlsx"
    # copepod counts from tows
    CBmatrix_fname = os.path.join(ZOO_DIR, cb_fname)
    if not os.path.isfile(CBmatrix_fname):
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, cb_fname,
                     to_path=ZOO_DIR)
    # mysids counts from tow
    my_fname = "1972-2017MysidMatrix.xlsx"
    mysid_fname = os.path.join(ZOO_DIR, my_fname)
    if not os.path.isfile(mysid_fname):
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, my_fname,
                     to_path=ZOO_DIR)
    # mysids counts on the pump samples
    pump_fname = "1972-2017PumpMatrix.xlsx"
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


if __name__ == "__main__":
    # get the root directory to set relative paths
    ROOT_DIR = os.pardir
    DATA_DIR = r"data"
    ZOO_DIR = os.path.join(ROOT_DIR, DATA_DIR, "ZOO")
    ftp_zooplankton_dir = "IEP_Zooplankton"
        
    data_portal_urls_file = "data_portal_urls.json"    
    data_portal_urls = get_urls_from_json_file(data_portal_urls_file)

    CDFW_FTP_ADDR = data_portal_urls["CDFW_FTP_ADDR"]   
    
    
    if not os.path.isdir(ZOO_DIR):
        os.mkdir(ZOO_DIR)
    get_zooplankton(CDFW_FTP_ADDR, ftp_zooplankton_dir, ZOO_DIR) 

    # IMPORT EMP PHYTOPLANKTON DATA
    phyto_data_path = os.path.join(ROOT_DIR, DATA_DIR, "PHYTO")
    if not os.path.isdir(phyto_data_path):
        os.mkdir(phyto_data_path)
    emp_phyto_filename = "emp_phytoplankton.csv"
    emp_phyto_path = os.path.join(phyto_data_path, emp_phyto_filename)
    EMP_PHYTOPLANKTON_URL = data_portal_urls["EMP_PHYTOPLANKTON_URL"]
    if not os.path.isfile(emp_phyto_path):
        emp_phyto = pd.read_csv(EMP_PHYTOPLANKTON_URL)
        emp_phyto.to_csv(emp_phyto_path)
    # IMPORT FISH DATA
    fish_path = os.path.join(ROOT_DIR, DATA_DIR, "FISH")
    if not os.path.isdir(fish_path):
        os.mkdir(fish_path) 
    # Retrieve data from the EDI data repos
    # YOLO BYP SALMON FISH
    ybp_salmon_filename = "ybp_salmon.csv"    
    ybp_salmon_path = os.path.join(fish_path, ybp_salmon_filename)
    YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL = data_portal_urls["YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL"]
    if not os.path.isfile(ybp_salmon_path):
        ybp_edi = requests.get(YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL).content
        ybp_salmon = pd.read_csv(io.StringIO(ybp_edi.decode("utf-8")))
        # save the file locally
        ybp_salmon.to_csv(ybp_salmon_path)
        
    # USFWS Delta Juvenile Fish Monitoring Program
    djfmp_filename =  "djfmp.csv"
    djfmp_path = os.path.join(fish_path, djfmp_filename)
    DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL = data_portal_urls["DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL"]

    if not os.path.isfile(djfmp_path):
        djfmps_edi = requests.get(DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL).content
        djfmp = pd.read_csv(io.StringIO(djfmps_edi.decode("utf-8")))
        # save the file locally
        djfmp.to_csv(djfmp_path)

    # move files from ftp to local space
    # TODO: ONLY COPY FILES IF AND ONLY IF THEY ARE UPDATED)
    # Smelt Larva Survey (CDFW): Longfin Smelt
    FTP_DS_DIR = "Delta Smelt"
    sls_filename = "SLS.mdb"
    sls_ds_path = os.path.join(fish_path, sls_filename)
    
    if not os.path.isfile(sls_ds_path):
        get_ftp_file(CDFW_FTP_ADDR, FTP_DS_DIR, sls_filename,
                     to_path=fish_path)
    
    # Spring Kodiak
    # Careful and be prepared to wait bc SKT is a large file (~400 MB)!
    skt_filename = "SKT.mdb"
    sls_ls_path = os.path.join(fish_path, skt_filename)
    if not os.path.isfile(sls_ls_path):
        get_ftp_file(CDFW_FTP_ADDR, FTP_DS_DIR, skt_filename,
                     to_path=fish_path)
    
    # Bay Study (CDFW): Longfin Smelt
    #FETCH THE DATA
    ls_smelt_filename_zip = "Bay Study_FishCatchMatrices_1980-2017.zip"
    ls_zip_file_path = os.path.join(fish_path, ls_smelt_filename_zip)
    FTP_LS_DIR = "BayStudy/CatchMatrices"
    if not os.path.isfile(ls_zip_file_path):
        
        get_ftp_file(CDFW_FTP_ADDR, FTP_LS_DIR,
                     ls_smelt_filename_zip,
                     to_path=fish_path)
    #UNZIP THE DATA
    BAYSTUDY_DIR = "BayStudy"
    ls_smelt_dir = os.path.join(fish_path, BAYSTUDY_DIR)
    if not os.path.isdir(ls_smelt_dir):
        os.mkdir(ls_smelt_dir)
    ls_smelt_filename = "Bay Study_MWT_1980-2017_FishMatrix.xlsx"
    ls_smelt_path = os.path.join(ls_smelt_dir, ls_smelt_filename)
                     
    if not os.path.isfile(ls_smelt_path):
        # unpack zip files if necessary
        zip_ref = zipfile.ZipFile(ls_smelt_filename_zip, "r")
        zip_ref.extractall(path=ls_smelt_path)
        zip_ref.close()
