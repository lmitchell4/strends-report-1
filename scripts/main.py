# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 17:06:44 2018
script to process some WDL data from the CNRA location
https://data.ca.gov/dataset/water-quality-data
@author: jsaracen
"""
# TODO:GROUPBY STATION AND AGG INTO REGIONS
import csv
from ftplib import FTP
import io
# import json
import os
import pandas as pd
import pyodbc
import requests
# from urllib.request import urlopen

#import zip file.
import zipfile
# for path checking.
import os.path
# deleting directory.
import shutil


def get_ftp_file(addr, ftp_path, fname, to_path=r'..\data', verbose=False):
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
            # iterate over zip info list.
            for item in zip_ref.infolist():
                zip_ref.extract(item, outloc)
            # once extraction is complete
            # check if the files contains any zip file or not .
            # if directory then go through the directoty.
#            zip_files = [files for files in zip_ref.filelist
#                         if files.filename.endswith('.zip')]
            # print other zip files
            # print(zip_files)
            # iterate over zip files.
#            if zip_files:
#                for file in zip_files:
                    # iterate to get the name.
#                    new_loc = os.path.join(outloc, file.filename)
                 # new location
                 # print(new_loc)

            # close.
            zip_ref.close()
            return # zip_files

root_dir = os.path.dirname(os.path.abspath(__file__))

# define paramters and sites of interest
sites = []
parameters = []
# read in the data file

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

 response = urlopen(data_url)
 string = response.read().decode('utf-8')
 json_obj = json.loads(string)
 this is a large (~1gb FILE, DONT PULL COMPLETELY)
 wdl_data_url = r'https://data.cnra.ca.gov/dataset/3f96977e-2597-4baa-8c9b-c433cea0685e/resource/a9e7ef50-54c3-4031-8e44-aa46f3c660fe/download/lab-results.csv'
 wdl_data = pd.read_csv(wdl_data_url)
"""

# IMPORT FLOW INDEX
flowindex_path = os.path.join(root_dir, 'FLOW',
                              'dayflowCalculations2017.csv').replace('scripts',
                                                                     'data')
flowindex = pd.read_csv(flowindex_path)
# import all flow data to date
flow_path = os.path.join(root_dir, 'flow',
                         'flow_1929-10-01_2017-09-30.csv').replace('scripts',
                                                                   'data')
flow = pd.read_csv(flow_path, index_col=[0])
flow.index = pd.to_datetime(flow.index)
# IMPORT ZOOPLANKTON
# Retrieve all ZOO files from an FTP (ftp://ftp.dfg.ca.gov/IEP_Zooplankton/)
# TODO: Convert counts to biomass using taxon specific weights

# Read from ftp directly
zoo_data_path = os.path.join(os.pardir, r"data\ZOO")

# dfg_zoo_ftp_path = 'ftp://ftp.dfg.ca.gov/IEP_Zooplankton'
# CBmatrix_path = os.path.join(dfg_zoo_ftp_path, '1972-2017CBMatrix.xlsx')
cdfw_ftp_path = 'ftp.dfg.ca.gov'
# Smelt Larva Survey (CDFW): Longfin Smelt
cb_fname = '1972-2017CBMatrix.xlsx'
get_ftp_file(cdfw_ftp_path, 'IEP_Zooplankton', cb_fname,
             to_path=zoo_data_path)
CBmatrix_path = os.path.join(zoo_data_path, cb_fname)


# Read data from flat files on local machine
#CBmatrix_path = os.path.join(root_dir, 'ZOO',
#                             cb_fname).replace('scripts', 'data')

CBmatrix = pd.read_excel(CBmatrix_path,
                         sheet_name='CB CPUE Matrix 1972-2017')

mysid_fname = '1972-2017MysidMatrix.xlsx'
#Mysidmatrix_path = os.path.join(root_dir, 'ZOO',
#                                mysid_fname).replace('scripts',
#                               'data')
get_ftp_file(cdfw_ftp_path, 'IEP_Zooplankton', mysid_fname,
             to_path=zoo_data_path)

Mysidmatrix_path = os.path.join(zoo_data_path, mysid_fname)
Mysidmatrix = pd.read_excel(Mysidmatrix_path,
                            sheet_name='Mysid CPUE Matrix 1972-2017')


pump_fname = '1972-2017PumpMatrix.xlsx'
#Pumpmatrix_path = os.path.join(root_dir, 'ZOO',
#                               pump_fname).replace('scripts', 'data')
Pumpmatrix_path = os.path.join(zoo_data_path, pump_fname)

Pumpmatrix = pd.read_excel(Pumpmatrix_path,
                           sheet_name='Pump CPUE Matrix 1972-2017')
# IMPORT PHYTO DATA

emp_phyto_url = r'https://emp.baydeltalive.com/assets/06942155460a79991fdf1b57f641b1b4/text/csv/Phytoplankton_Algal_Type_Data_1975_-2016.csv'
emp_phyto = pd.read_csv(emp_phyto_url)



# IMPORT FISH DATA
data_path = os.path.join(os.pardir, r"data\FISH")
# From EDI repos
#YOLO BYP SALMON FISH
ybp_salmon_url = r'http://pasta.lternet.edu/package/data/eml/edi/233/1/8b5ba731b0956bf719d3abaacdda5c70'
ybp_edi = requests.get(ybp_salmon_url).content
ybp_salmon = pd.read_csv(io.StringIO(ybp_edi.decode('utf-8')))
# save the file locally
ybp_salmon.to_csv(os.path.join(data_path, 'ybp_salmon.csv'))
# USFWS Delta Juvenile Fish Monitoring Program
djfmp_url = r'https://pasta.lternet.edu/package/data/eml/edi/244/2/1c7e55b76e6455b3093f6a66cb3ba38c'
djfmps_edi = requests.get(djfmp_url).content
djfmp = pd.read_csv(io.StringIO(djfmps_edi.decode('utf-8')))
# save the file locally
djfmp.to_csv(os.path.join(data_path, 'djfmp.csv'))

# move files from ftp to local space
# TODO: ONLY COPY FILES IF AND ONLY IF THEY ARE UPDATED)

# Smelt Larva Survey (CDFW): Longfin Smelt
sls_fname = 'SLS.mdb'
get_ftp_file(cdfw_ftp_path, 'Delta Smelt', sls_fname, to_path=data_path)
sls_ds_path = os.path.join(data_path, sls_fname)

# Spring Kodiak
skt_fname = 'SKT.mdb'
# Careful and be prepared to wait bc SKT is a large file (~400 MB)!
get_ftp_file(cdfw_ftp_path, 'Delta Smelt', skt_fname, to_path=data_path)
skt_ls_path = os.path.join(data_path, skt_fname)

# Bay Study (CDFW): Longfin Smelt
ls_smelt_fname_zip = 'Bay Study_FishCatchMatrices_1980-2017.zip'
get_ftp_file(cdfw_ftp_path, 'BayStudy/CatchMatrices', ls_smelt_fname_zip,
             to_path=data_path)

# unpack zip files
path_to_zip_file = os.path.join(data_path, ls_smelt_fname_zip)
zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
ls_smelt_path = os.path.join(data_path, 'BayStudy')
zip_ref.extractall(path=ls_smelt_path)
zip_ref.close()
ls_smelt_fname = os.path.join(ls_smelt_path,
                              'Bay Study_MWT_1980-2017_FishMatrix.xlsx')
# read in data
ls_smelt = pd.read_excel(ls_smelt_fname, sheet_name='MWT Catch Matrix')
ls_smelt['Datetime'] = pd.to_datetime(ls_smelt['Date'])
# create a multi-indexed dataframe based on date and station of smelt data
ls_smelt.set_index(['Datetime', 'Station'], inplace=True)

# connect to CDFW access database files
MDB = sls_ds_path #sls_ds_path
DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'
PWD = 'pw'
# connect to db
con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV, MDB, PWD))
cur = con.cursor()

# run a query and get the results
SQL = 'SELECT * FROM Catch;'  # catch query
rows = cur.execute(SQL).fetchall()
cur.close()
con.close()

# you could change the mode from 'w' to 'a' (append) for any subsequent queries
with open('catch_table.csv', 'wb') as fou:
    csv_writer = csv.writer(fou)  # default field-delimiter is ","
    csv_writer.writerows(rows)
