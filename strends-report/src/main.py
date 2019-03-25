# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 17:06:44 2018
script to run the status and trends data aggregation tool
https://data.ca.gov/dataset/water-quality-data
@author: jsaracen
"""
from fetch import fetch_data_files
from read import read_data_files, write_postgresql_table_names
import os
import pickle
#from store import store_data_files
from base import engine, Base
import psycopg2
#TODO:* Create database schema
#TODO:* Speed up writing dataframes to database 
#TODO:* Add logging
#TODO:* Pass arguments from command line using argparse
#TODO:* Run this script from a bash file on a task

def fetch_data():
    fetch_data_files()
    
def read_data(FILE_PATHS_FILENAME):
    return read_data_files(FILE_PATHS_FILENAME)

def store_data(data):
    try:        
        Base.metadata.create_all(engine)
        print('Storing data...')        
        for table_name, df in data.items():
            try:
                print('Storing {} to database'.format(table_name.lower()))
                #TODO: Easy but slow so speed this up!
                df.to_sql(table_name, engine, if_exists="replace",
                          chunksize=1000)
            except:
                print('Could not store {} to database, check database connection {} and try again'.format(table_name.lower()), engine)
                
    except psycopg2.OperationalError:
        print("Couldn''t connect to database, make sure its running and try again")
    print ("Database updated with current data")
    return

def query_data():
    """query data for plotting"""
    pass

def main(store=False):
    """main entry point for the script"""
    FILE_PATHS_FILENAME = "file_paths.json" 
    fetch_data()
    data = read_data(FILE_PATHS_FILENAME)
    
    if store:
        write_postgresql_table_names(data)
        store_data(data)    
    return data

if __name__ == "__main__":
    data = main(store=True)
    #save it to a pickle for later viewing
    PICKLED_DATA_PATH = os.path.join(os.pardir, 'results', 'data.pickle')
    with open(PICKLED_DATA_PATH, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #load it to a pickle for later viewing

    with open(PICKLED_DATA_PATH, 'rb') as handle:
        b = pickle.load(handle)
    