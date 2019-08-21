# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 18:21:11 2018
script to fetch data from various repositories and online data locations
@author: jsaracen
"""

from bs4 import BeautifulSoup
from ftplib import FTP
import ftplib
import io
import numpy as np
import os
from pathlib import Path
import pandas as pd
import requests
import sys
import zipfile
#from setup_paths import * #LS_SMELT_PATH, YBP_SALMON_PATH SKT_LS_PATH', 'SLS_DS_PATH', 'DJFMP_PATH', 'EMP_PHYTO_PATH', 'LS_ZIP_FILE_PATH', 'FLOW_INDEX_PATH', 'WQ_FIELD_PATH', 'WQ_LAB_PATH', 'WDL_WQ_PATH', 'ZOOPLANKTON_MYSID_PATH', 'ZOOPLANKTON_CBMATRIX_PATH', 'ZOOPLANKTON_PUMP_PATH'
#from setup_paths import FLOW_INDEX_FILENAME,EMP_PHYTOPLANKTON_FILENAME,ZOOPLANKTON_MYSID_FILENAME,ZOOPLANKTON_PUMP_FILENAME,ZOOPLANKTON_CBMATRIX_FILENAME
#from setup_paths import LS_SMELT_FILENAME, YBP_SALMON_FILENAME,DELTA_JUVENILE_FISH_MONITORING_PROGRAM_FILENAME
#from setup_paths import WQ_LAB_FILENAME, WQ_FIELD_FILENAME, WDL_WQ
from setup_paths import LS_SMELT_FILENAME_ZIP, SLS_FILENAME,SKT_FILENAME, USFWS_REDBLUFF_SALMON_PATH, CDFW_FMWT_PATH,USFWS_REDBLUFF_SALMON_URL,CDFW_FMWT_URL
from setup_paths import EMP_PHYTO_PATH, YBP_SALMON_PATH, DJFMP_PATH, SKT_DS_PATH, LS_SMELT_PATH, LS_ZIP_FILE_PATH, SLS_LS_PATH
from setup_paths import CDFW_FTP_ADDR, FTP_ZOO_DIR, ZOO_DIR, FISH_DIR, FTP_LS_DIR, FTP_DS_DIR, LS_SMELT_DIR
from setup_paths import DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL, EMP_PHYTOPLANKTON_URL, YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL
from setup_paths import data_filenames


def data_pull_message(fileconfig):
    print('No local copy of {}, so we will now download it...'.format(fileconfig.absolute(),))
    return


def get_ftp_file(addr, ftp_path, fname, to_path="", verbose=True):
    """ Function to grab a file, fname, from an ftp specified by addr
    at the given path and put in the local directory"""
    try:
        ftp = FTP(addr)
        if verbose:
            ftp.set_debuglevel(1)
        ftp.login()
        if verbose:
            print("Welcome: ", ftp.getwelcome())
            ftp.retrlines("LIST")
        ftp.cwd(ftp_path)
        local_filename = os.path.join(to_path,  fname)
        filedata = open(local_filename, "wb")
        #get the size fo the file
        filesize = ftp.size(fname)
        #TODO: add conditional to only get the file if the size on server 
        # is greater than the size of the local copy, which is passed in
        #retrieve the file
        ftp.retrbinary("RETR " + fname, filedata.write)
        if verbose:
            print("Retrieving file:", fname)
        filedata.close()
        ftp.quit()
    except ftplib.all_errors as error:
        print("ftplib error: {0}".format(error))
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        return filesize
    return 


def get_zooplankton(CDFW_FTP_ADDR, ftp_zooplankton_dir, ZOO_DIR, filenames):
    """ Funtion to pull ZOOPLANKTON workbooks from CDFW's FTP site"""
    
    cb_fname = filenames.get('ZOOPLANKTON_CBMATRIX_FILENAME',
                             "1972-2017CBMatrix.xlsx")
    # copepod counts from tows
    CBmatrix_fname = os.path.join(ZOO_DIR, cb_fname)
    fileconfig = Path(CBmatrix_fname)
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, cb_fname,
                     to_path=ZOO_DIR)
    # mysids counts from tow
    my_fname = filenames.get('ZOOPLANKTON_MYSID_FILENAME',
                             "1972-2017MysidMatrix.xlsx")
    mysid_fname = os.path.join(ZOO_DIR, my_fname)
    fileconfig = Path(mysid_fname)
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, my_fname,
                     to_path=ZOO_DIR)
    # mysids counts on the pump samples
    pump_fname = filenames.get('ZOOPLANKTON_PUMP_FILENAME',
                               "1972-2017PumpMatrix.xlsx")
    Pumpmatrix_fname = os.path.join(ZOO_DIR, pump_fname)
    fileconfig = Path(Pumpmatrix_fname)
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        get_ftp_file(CDFW_FTP_ADDR, ftp_zooplankton_dir, pump_fname,
                     to_path=ZOO_DIR)


def extractzip(loc, outloc):
        """
        using the zipfile tool extract here .
        This function is valid if the file type is zip only
        from Reezoo Bose (stackoverflow)
       """
        with zipfile.ZipFile(loc, "r") as zip_ref:
            print("Unpacking", loc, "to", outloc, "...")
            # iterate over zip info list.
            for item in zip_ref.infolist():
                zip_ref.extract(item, outloc)
            zip_ref.close()
            return  # zip_files

def query_redbluff_data(url, start_year, end_year):
    year_data = []
    for year in np.arange(start_year, end_year+1):
#        url = f'http://www.cbr.washington.edu/sacramento/data/php/rpt/redbluff_daily.php?outputFormat=csv&year={year}&biweekly=other&wtemp=default'
        url = url.format(year=year)
        year_data.append(pd.read_csv(url, na_values=['NA'], skipfooter=7, engine='python'))
    dataframe = pd.concat(year_data)
    #dataframe.index=pd.to_datetime(dataframe['Date'])
    return dataframe


def scrape_fmwt(url, table_number, cols, species):
    ''' Function to scrape data from the cdfw fmwt webpage
    and return data as a pandas dataframe.There are six
     tables for the various fish species'''
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[table_number] 
    dataframe = pd.DataFrame(pd.read_html(str(table))[0])
    dataframe.columns = cols
   # dataframe.index = pd.to_datetime(dataframe['Year'].astype(int),format='%Y')
    dataframe['Species'] = species
    return dataframe

def query_fmwt(url):
    list_of_species = ['Age_0_Striped_Bass', 'Delta_Smelt', 'Longfin_Smelt',
                   'American_Shad', 'Splittail', 'Threadfin_Shad']
    list_of_counts = []
    columns = ['Year', 'Sept', 'Oct', 'Nov', 'Dec', 'Total']
    for i, species in enumerate(list_of_species):
        list_of_counts.append(scrape_fmwt(url, i, columns, species))
    #combine species into long form
    all_species = pd.concat(list_of_counts)
    return all_species

#TODO: Add try/except clauses for each data fetching routines
#TODO: Only fetch the data if local copy is out of date with remote copy
def fetch_data_files():
        ### SETUP DATA SOURCE LOCATIONS, DIRECTORIES, PATHS###
    # get the root directory of this script to set relative paths
    print("Fetching data...")
    path_to_certs = os.environ['REQUESTS_CA_BUNDLE']

    get_zooplankton(CDFW_FTP_ADDR, FTP_ZOO_DIR, ZOO_DIR, data_filenames)
    fileconfig = Path(EMP_PHYTO_PATH)
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        emp_phyto = pd.read_csv(EMP_PHYTOPLANKTON_URL)
        emp_phyto.to_csv(EMP_PHYTO_PATH, index=False)   
    # IMPORT FISH DATA
    
    fileconfig = Path(CDFW_FMWT_PATH)
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        CDFW_FMWT_counts = query_fmwt(CDFW_FMWT_URL)
        CDFW_FMWT_counts.to_csv(CDFW_FMWT_PATH,index=False)

    fileconfig = Path(USFWS_REDBLUFF_SALMON_PATH)
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        redbluff_salmon = query_redbluff_data(USFWS_REDBLUFF_SALMON_URL, 2004, 2019) #TODO: make these years configureable
        redbluff_salmon.to_csv(USFWS_REDBLUFF_SALMON_PATH, index=False)
    
    # Retrieve data from the EDI data repos
    # YOLO BYP SALMON FISH    
    fileconfig = Path(YBP_SALMON_PATH)
    #TODO: write a helper function to pull data from EDI
    #  YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL= r'https://portal.edirepository.org/nis/dataviewer?packageid=edi.233.2&entityid=015e494911cf35c90089ced5a3127334'
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        try:
            ybp_edi = requests.get(YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL,
                                   verify=path_to_certs).content
            ybp_salmon = pd.read_csv(io.StringIO(ybp_edi.decode("utf-8")))
        except:
            print("Couldn''t download data from {}".format(YOLO_BYPASS_FISH_MONITORING_PROGRAM_URL))
            ybp_salmon = pd.DataFrame()
        finally:
            # save the file locally
            ybp_salmon.to_csv(YBP_SALMON_PATH, index=False)            
    # USFWS Delta Juvenile Fish Monitoring Program
    fileconfig = Path(DJFMP_PATH)    
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        try:
            djfmps_edi = requests.get(DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL,
                                      verify=path_to_certs).content
            djfmp = pd.read_csv(io.StringIO(djfmps_edi.decode("utf-8")))
        except:
            print("Couldn''t download data from {}".format(DELTA_JUVENILE_FISH_MONITORING_PROGRAM_URL))
            djfmp = pd.DataFrame()
        finally:
        # save the file locally
            djfmp.to_csv(DJFMP_PATH, index=False)
    # move files from ftp to local space
    # TODO: ONLY COPY FILES IF AND ONLY IF THEY ARE UPDATED)
    # Smelt Larva Survey (CDFW): Longfin Smelt
    fileconfig = Path(SLS_LS_PATH)
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        get_ftp_file(CDFW_FTP_ADDR, FTP_DS_DIR, SLS_FILENAME,
                     to_path=FISH_DIR)
    # Spring Kodiak
    # Careful and be prepared to wait bc SKT is a large file (~400 MB)!
    fileconfig = Path(SKT_DS_PATH)
    if not fileconfig.is_file():
        data_pull_message(fileconfig)
        get_ftp_file(CDFW_FTP_ADDR, FTP_DS_DIR, SKT_FILENAME,
                     to_path=FISH_DIR)
    # Bay Study (CDFW): Longfin Smelt
    #FETCH THE DATA
    fileconfig =  Path(LS_ZIP_FILE_PATH)
    if not fileconfig.is_file():        
        data_pull_message(fileconfig)
        get_ftp_file(CDFW_FTP_ADDR, FTP_LS_DIR,
                     LS_SMELT_FILENAME_ZIP,
                     to_path=FISH_DIR)
    fileconfig = Path(LS_SMELT_PATH)             
    if not fileconfig.is_file():
        print("Unzipping {}".format(LS_SMELT_PATH))
        # unpack zip files if necessary
        zip_ref = zipfile.ZipFile(LS_ZIP_FILE_PATH, "r")
        zip_ref.extractall(path=LS_SMELT_DIR)
        zip_ref.close()


def main():
    """main entry point for the script"""
    fetch_data_files()
    return


if __name__ == "__main__":
    sys.exit(main())