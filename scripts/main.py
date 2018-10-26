# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 17:06:44 2018
script to process some WDL data from the CNRA location
https://data.ca.gov/dataset/water-quality-data
@author: jsaracen
"""
#TODO:GROUPBY STATION AND AGG INTO REGIONS
import os
import pandas as pd
from urllib.request import urlopen
import requests
import io
#import json



root_dir = os.path.dirname(os.path.abspath(__file__))

#define paramters and sites of interest
sites=[]
parameters=[]
#read in the data file
#df = pd.read_csv(r'J:\Status and Trends\data\lab-results.csv')
##select only surface water samples
#sw = df[(df['STATION_TYPE']=='Surface Water')]
##grab and sort a list of the available sw parameters 
#sw_paramters = sorted(list(sw['PARAMETER'].unique()))
##start selecting paramters
#wq = sw[(sw['PARAMETER']=='Dissolved Nitrate') |
#        (sw['PARAMETER']=='Dissolved Ammonia')] 
#       

#CKAN API to GET WDL DATA
#LAB DATA
#station_url = 'https://data.cnra.ca.gov/api/3/action/datastore_search?resource_id=24fc759a-ff0b-479a-a72a-c91a9384540f&limit=5&q=title:jones'  
#data_url = 'https://data.cnra.ca.gov/api/3/action/datastore_search?resource_id=a9e7ef50-54c3-4031-8e44-aa46f3c660fe&limit=5&q=title:jones'
  
#response = urlopen(data_url)
#string = response.read().decode('utf-8')
#json_obj = json.loads(string)
#this is a large (~1gb FILE, DONT PULL COMPLETELY)
#wdl_data_url = r'https://data.cnra.ca.gov/dataset/3f96977e-2597-4baa-8c9b-c433cea0685e/resource/a9e7ef50-54c3-4031-8e44-aa46f3c660fe/download/lab-results.csv'
#wdl_data = pd.read_csv(wdl_data_url)
#IMPORT FLOW INDEX
flowindex_path = os.path.join(root_dir, 'FLOW', 'dayflowCalculations2017.csv').replace('scripts','data')
flowindex = pd.read_csv(flowindex_path)
#import all flow data to date
flow_path = os.path.join(root_dir, 'flow', 'flow_1929-10-01_2017-09-30.csv').replace('scripts','data')
flow = pd.read_csv(flow_path, index_col = [0])
flow.index = pd.to_datetime(flow.index)
#IMPORT ZOOPLANKTON
#convert counts to biomass using taxon specific weights
CBmatrix_path = os.path.join(root_dir, 'ZOO', '1972-2017CBMatrix.xlsx').replace('scripts','data')
CBmatrix = pd.read_excel(CBmatrix_path, sheet_name='CB CPUE Matrix 1972-2017')
Mysidmatrix_path = os.path.join(root_dir, 'ZOO', '1972-2017MysidMatrix.xlsx').replace('scripts','data')
Mysidmatrix  = pd.read_excel(Mysidmatrix_path, sheet_name='Mysid CPUE Matrix 1972-2017')
Pumpmatrix_path = os.path.join(root_dir, 'ZOO', '1972-2017PumpMatrix.xlsx').replace('scripts','data')
Pumpmatrix = pd.read_excel(Pumpmatrix_path, sheet_name='Pump CPUE Matrix 1972-2017')
#IMPORT PHYTO DATA

emp_phyto_url = r'https://emp.baydeltalive.com/assets/06942155460a79991fdf1b57f641b1b4/text/csv/Phytoplankton_Algal_Type_Data_1975_-2016.csv'
emp_phyto = pd.read_csv(emp_phyto_url)

ybp_salmon_url = r'http://pasta.lternet.edu/package/data/eml/edi/233/1/8b5ba731b0956bf719d3abaacdda5c70'
s = requests.get(ybp_salmon_url).content
ybp_salmon = pd.read_csv(io.StringIO(s.decode('utf-8')))


#read in CDFW databases

