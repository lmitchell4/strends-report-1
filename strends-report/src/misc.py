# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 18:36:43 2018
misc functions to deal with files
@author: jsaracen
"""

# TODO:GROUPBY STATION AND AGG INTO REGIONS
# import csv
# import json

# import zip file.
import glob
import os
import pandas as pd


def list_of_files(path, fmatch):
#    path = r'C:\Users\saraceno\Documents\Code\Python\WEBB\SS_PSDS'
#    fmatch = '*$ls.txt'
    files = []
    for name in glob.glob(os.path.join(path, fmatch)):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files

def concat_emp_files(files_dir):
    field_files = list_of_files(files_dir, "Field*.xlsx")
    lab_files =  list_of_files(files_dir, "Lab*.xlsx")
    
    
    pd.concat([pd.read_excel(f) for f in field_files],
               axis=0).to_excel(os.path.join(files_dir, "emp_field_data.xlsx"),
                     index=False)
    pd.concat([pd.read_excel(f) for f in lab_files],
               axis=0).to_excel(os.path.join(files_dir, "emp_lab_data.xlsx"),
                     index=False)

    return
# you could change the mode from 'w' to 'a' (append) for any subsequent queries
#with open(sls_db_fname.replace('.mdb','.csv'), 'wb') as fou:
#    csv_writer = csv.writer(fou)  # default field-delimiter is ","
#    csv_writer.writerows(rows)
   # concatenate a bunch of individual files
files_dir = r'\data\WQ\baydeltalive'
concat_emp_files(files_dir)
#field_files = list_of_files(files_dir, "Field*.xlsx")
#lab_files =  list_of_files(files_dir, "Lab*.xlsx")
#pd.concat([pd.read_excel(f) for f in lab_files], axis=0).to_excel("emp_lab_data.xlsx", index=False)
data = dict()


keys=[]
column_names = []
for name, df in data.items():
    column_names.append(df.columns.tolist())
    keys.append(name.lower())
columns = pd.DataFrame(index=keys, data=column_names).T
columns.to_excel('columns.xlsx',index=False)



#BEGIN BUILDING A POSTGRES DATABASE USING SQLAlchemy 
#files_dir = os.path.join(os.pardir,"data","WQ")

"""
    df = pd.read_csv(r'J:\Status and Trends\data\lab-results.csv')
    # select only surface water samples
    sw = df[(df['STATION_TYPE']=='Surface Water')]
    # grab and sort a list of the available sw parameters
    sw_paramters = sorted(list(sw['PARAMETER'].unique()))
    # start selecting paramters
    wq = sw[(sw['PARAMETER']=='Dissolved Nitrate') |
            (sw['PARAMETER']=='Dissolved Ammonia')]
    # CKAN API to GET WDL DATA
    # LAB DATA
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
    
