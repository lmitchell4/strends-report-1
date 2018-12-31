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

def get_zooplankton(CDFW_FTP_ADDR, ftp_zoo_dir, zoo_path):
    cb_fname = "1972-2017CBMatrix.xlsx"
    # copepod counts from tows
    CBmatrix_fname = os.path.join(zoo_path, cb_fname)
    if not os.path.isfile(CBmatrix_fname):
        get_ftp_file(CDFW_FTP_ADDR, ftp_zoo_dir, cb_fname,
                     to_path=zoo_path)
    # mysids counts from tow
    my_fname = "1972-2017MysidMatrix.xlsx"
    mysid_fname = os.path.join(zoo_path, my_fname)
    if not os.path.isfile(mysid_fname):
        get_ftp_file(CDFW_FTP_ADDR, ftp_zoo_dir, my_fname,
                     to_path=zoo_path)
    # mysids counts on the pump samples
    pump_fname = "1972-2017PumpMatrix.xlsx"
    Pumpmatrix_fname = os.path.join(zoo_path, pump_fname)
    if not os.path.isfile(Pumpmatrix_fname):
        get_ftp_file(CDFW_FTP_ADDR, ftp_zoo_dir, pump_fname,
                     to_path=zoo_path)


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
    zoo_path = os.path.join(ROOT_DIR, r"data\ZOO")
    ftp_zoo_dir = "IEP_Zooplankton"
        
    data_portal_urls_file = "data_portal_urls.json"
    data_portal_urls = get_urls_from_json_file(data_portal_urls_file)
    CDFW_FTP_ADDR = data_portal_urls["CDFW_FTP_ADDR"]
    if not os.path.isdir(zoo_path):
        os.mkdir(zoo_path)
    get_zooplankton(CDFW_FTP_ADDR, ftp_zoo_dir, zoo_path) 

    # IMPORT EMP PHYTOPLANKTON DATA
    phyto_data_path = os.path.join(ROOT_DIR, r"data\PHYTO")
    if not os.path.isdir(phyto_data_path):
        os.mkdir(phyto_data_path)
    emp_phyto_fname = os.path.join(phyto_data_path, "emp_phytoplankton.csv")
    EMP_PHYTOPLANKTON_URL = data_portal_urls["EMP_PHYTOPLANKTON_URL"]
    if not os.path.isfile(emp_phyto_fname):
        emp_phyto = pd.read_csv(EMP_PHYTOPLANKTON_URL)
        emp_phyto.to_csv(emp_phyto_fname)
    # IMPORT FISH DATA
    fish_path = os.path.join(ROOT_DIR, r"data\FISH")
    if not os.path.isdir(fish_path):
        os.mkdir(fish_path) 
    # Retrieve data from the EDI data repos
    # YOLO BYP SALMON FISH
    ybp_salmon_fname = os.path.join(fish_path, "ybp_salmon.csv")
    YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL = data_portal_urls["YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL"]
    if not os.path.isfile(ybp_salmon_fname):
        ybp_edi = requests.get(YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL).content
        ybp_salmon = pd.read_csv(io.StringIO(ybp_edi.decode("utf-8")))
        # save the file locally
        ybp_salmon.to_csv(ybp_salmon_fname)
        
    # USFWS Delta Juvenile Fish Monitoring Program
    djfmp_fname = os.path.join(fish_path, "djfmp.csv")
    DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL = data_portal_urls["DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL"]

    if not os.path.isfile(djfmp_fname):
        djfmps_edi = requests.get(DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL).content
        djfmp = pd.read_csv(io.StringIO(djfmps_edi.decode("utf-8")))
        # save the file locally
        djfmp.to_csv(djfmp_fname)

    # move files from ftp to local space
    # TODO: ONLY COPY FILES IF AND ONLY IF THEY ARE UPDATED)
    # Smelt Larva Survey (CDFW): Longfin Smelt
    ftp_fish_path = "Delta Smelt"
    sls_fname = "SLS.mdb"
    sls_ds_path = os.path.join(fish_path, sls_fname)
    
    if not os.path.isfile(sls_ds_path):
        get_ftp_file(CDFW_FTP_ADDR, ftp_fish_path, sls_fname,
                     to_path=fish_path)
    
    # Spring Kodiak
    # Careful and be prepared to wait bc SKT is a large file (~400 MB)!
    skt_fname = "SKT.mdb"
    sls_ls_path = os.path.join(fish_path, skt_fname)
    if not os.path.isfile(sls_ls_path):
        get_ftp_file(CDFW_FTP_ADDR, ftp_fish_path, skt_fname,
                     to_path=fish_path)
    
    # Bay Study (CDFW): Longfin Smelt
    #FETCH THE DATA
    ls_smelt_fname_zip = "Bay Study_FishCatchMatrices_1980-2017.zip"
    ls_zip_file = os.path.join(fish_path, ls_smelt_fname_zip)
    if not os.path.isfile(ls_zip_file):
        get_ftp_file(CDFW_FTP_ADDR, "BayStudy/CatchMatrices",
                     ls_smelt_fname_zip,
                     to_path=fish_path)
    #UNZIP THE DATA
    ls_smelt_path = os.path.join(fish_path, "BayStudy")
    if not os.path.isdir(ls_smelt_path):
        os.mkdir(ls_smelt_path)
    ls_smelt_name = "Bay Study_MWT_1980-2017_FishMatrix.xlsx"
    ls_smelt_fname = os.path.join(ls_smelt_path, ls_smelt_name)
                     
    if not os.path.isfile(ls_smelt_fname):
        # unpack zip files if necessary
        zip_ref = zipfile.ZipFile(ls_zip_file, "r")
        zip_ref.extractall(path=ls_smelt_path)
        zip_ref.close()
