# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 18:21:11 2018
script to fetch data from various repositories
@author: jsaracen
"""


from ftplib import FTP
import io
# import json
import os
import os.path
import pandas as pd
import pyodbc
import requests
# from urllib.request import urlopen

# import zip file.
import zipfile

def get_ftp_file(addr, ftp_path, fname, to_path='', verbose=False):
    """ Function to grab a file, fname, from an ftp specified by addr
    at the given path and put in the local directory"""
    ftp = FTP(addr)
    ftp.login()
    if verbose:
        print("Welcome: ", ftp.getwelcome())
        ftp.retrlines('LIST')
    ftp.cwd(ftp_path)
    local_filename = os.path.join(to_path,  fname)
    filedata = open(local_filename, 'wb')

    ftp.retrbinary('RETR ' + fname, filedata.write)
    if verbose:
        print('Retrieving file:', fname)
    filedata.close()
    ftp.quit()
    return


def extractzip(loc, outloc):
        '''
        using the zipfile tool extract here .
        This function is valid if the file type is zip only
        from Reezoo Bose (stackoverflow)
       '''
        with zipfile.ZipFile(loc, "r") as zip_ref:
            print("Unpacking",loc, "to", outloc, "...")
            # iterate over zip info list.
            for item in zip_ref.infolist():
                zip_ref.extract(item, outloc)

            zip_ref.close()
            return  # zip_files

if __name__ == "__main__":

    # get the root directory to find relative paths
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # define paramters and sites of interest
    sites = []
    parameters = []
    # read in the data file
    
    # TODO: split this main into several working scripts
    # 1) move data retrieval code to a separate script
    # 2) read data files and build sqlalchemy db
    # 3) etc
    """
    df = pd.read_csv(r'J:\Status and Trends\data\lab-results.csv')
    # select only surface water samples
    sw = df[(df['STATION_TYPE']=='Surface Water')]
    # grab and sort a list of the available sw parameters
    sw_paramters = sorted(list(sw['PARAMETER'].unique()))
    # start selecting paramters
    wq = sw[(sw['PARAMETER']=='Dissolved Nitrate') |
            (sw['PARAMETER']=='Dissolved Ammonia')]
    """
    # CKAN API to GET WDL DATA
    # LAB DATA
    """
     station_url = 'https://data.cnra.ca.gov/api/3/action/datastore_search?resource_id=24fc759a-ff0b-479a-a72a-c91a9384540f&limit=5&q=title:jones'
     data_url = 'https://data.cnra.ca.gov/api/3/action/datastore_search?resource_id=a9e7ef50-54c3-4031-8e44-aa46f3c660fe&limit=5&q=title:jones'
    # CKAN API
     response = urlopen(data_url)
     string = response.read().decode('utf-8')
     json_obj = json.loads(string)
     this is a large (~1gb FILE, DONT PULL COMPLETELY)
     wdl_data_url = r'https://data.cnra.ca.gov/dataset/3f96977e-2597-4baa-8c9b-c433cea0685e/resource/a9e7ef50-54c3-4031-8e44-aa46f3c660fe/download/lab-results.csv'
     wdl_data = pd.read_csv(wdl_data_url)
"""
    
    # IMPORT FLOW
    # FLOW INDEX DATA
    flow_path = os.path.join(os.pardir, r"data\FLOW")
    flowindex_fname = os.path.join(flow_path, 'dayflowCalculations2017.csv')
    flowindex = pd.read_csv(flowindex_fname)
    # import all flow data to date
    outflow_fname = os.path.join(flow_path, 'flow_1929-10-01_2017-09-30.csv')
    outflow = pd.read_csv(outflow_fname, index_col=[0])
    outflow.index = pd.to_datetime(outflow.index)
    
    # IMPORT ZOOPLANKTON
    # TODO: Convert counts to biomass using taxon specific weights
    zoo_path = os.path.join(os.pardir, r"data\ZOO")
    # Read from ftp directly
    # Retrieve all ZOO files from an FTP (ftp://ftp.dfg.ca.gov/IEP_Zooplankton/)
    cdfw_ftp_addr = 'ftp.dfg.ca.gov'
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
    
    # IMPORT PHYTO DATA
    phyto_data_path = os.path.join(os.pardir, r"data\PHYTO")
    emp_phyto_fname = os.path.join(phyto_data_path, 'emp_phytoplankton.csv')
    if not os.path.isfile(emp_phyto_fname):
        emp_phyto_url = r'https://emp.baydeltalive.com/assets/06942155460a79991fdf1b57f641b1b4/text/csv/Phytoplankton_Algal_Type_Data_1975_-2016.csv'
        emp_phyto = pd.read_csv(emp_phyto_url)
    else:
        emp_phyto = pd.read_csv(emp_phyto_fname)
    
    # IMPORT FISH DATA
    fish_path = os.path.join(os.pardir, r"data\FISH")
    # Retrieve data from the EDI data repos
    # YOLO BYP SALMON FISH
    ybp_salmon_fname = os.path.join(fish_path, 'ybp_salmon.csv')
    if not os.path.isfile(ybp_salmon_fname):
        ybp_salmon_url = r'http://pasta.lternet.edu/package/data/eml/edi/233/1/8b5ba731b0956bf719d3abaacdda5c70'
        ybp_edi = requests.get(ybp_salmon_url).content
        ybp_salmon = pd.read_csv(io.StringIO(ybp_edi.decode('utf-8')))
        # save the file locally
        ybp_salmon.to_csv(os.path.joinybp_salmon_fname)
    else:
        ybp_salmon = pd.read_csv(ybp_salmon_fname)
        
    # USFWS Delta Juvenile Fish Monitoring Program
    djfmp_fname = os.path.join(fish_path, 'djfmp.csv')
    if not os.path.isfile(djfmp_fname):
        djfmp_url = r'https://pasta.lternet.edu/package/data/eml/edi/244/2/1c7e55b76e6455b3093f6a66cb3ba38c'
        djfmps_edi = requests.get(djfmp_url).content
        djfmp = pd.read_csv(io.StringIO(djfmps_edi.decode('utf-8')))
        # save the file locally
        djfmp.to_csv(djfmp_fname)
    else:
        djfmp = pd.read_csv(djfmp_fname)
    # move files from ftp to local space
    # TODO: ONLY COPY FILES IF AND ONLY IF THEY ARE UPDATED)
    cdfw_ftp_addr = 'ftp.dfg.ca.gov'
    # Smelt Larva Survey (CDFW): Longfin Smelt
    ftp_fish_path = 'Delta Smelt'
    sls_fname = 'SLS.mdb'
    sls_ds_path = os.path.join(fish_path, sls_fname)
    if not os.path.isfile(sls_ds_path):
        get_ftp_file(cdfw_ftp_addr, ftp_fish_path, sls_fname,
                     to_path=fish_path)
    
    # Spring Kodiak
    # Careful and be prepared to wait bc SKT is a large file (~400 MB)!
    skt_fname = 'SKT.mdb'
    sls_ls_path = os.path.join(fish_path, skt_fname)
    if not os.path.isfile(sls_ls_path):
        get_ftp_file(cdfw_ftp_addr, ftp_fish_path, skt_fname,
                     to_path=fish_path)
    
    # Bay Study (CDFW): Longfin Smelt
    ls_smelt_fname_zip = 'Bay Study_FishCatchMatrices_1980-2017.zip'
    ls_zip_file = os.path.join(fish_path, ls_smelt_fname_zip)
    if not os.path.isfile(ls_zip_file):
        get_ftp_file(cdfw_ftp_addr, 'BayStudy/CatchMatrices',
                     ls_smelt_fname_zip,
                     to_path=fish_path)
    
    ls_smelt_path = os.path.join(fish_path, 'BayStudy')
    ls_smelt_name = 'Bay Study_MWT_1980-2017_FishMatrix.xlsx'
    ls_smelt_fname = os.path.join(ls_smelt_path, ls_smelt_name)
                     
    if not os.path.isfile(ls_smelt_fname):
        # unpack zip files if necessary
        zip_ref = zipfile.ZipFile(ls_zip_file, 'r')
        zip_ref.extractall(path=ls_smelt_path)
        zip_ref.close()
