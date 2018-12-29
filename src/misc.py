# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 18:36:43 2018
misc
@author: jsaracen
"""

# TODO:GROUPBY STATION AND AGG INTO REGIONS
# import csv
# import json

# import zip file.


# you could change the mode from 'w' to 'a' (append) for any subsequent queries
#with open(sls_db_fname.replace('.mdb','.csv'), 'wb') as fou:
#    csv_writer = csv.writer(fou)  # default field-delimiter is ","
#    csv_writer.writerows(rows)

#BEGIN BUILDING A POSTGRES DATABASE USING SQLAlchemy 


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
    
