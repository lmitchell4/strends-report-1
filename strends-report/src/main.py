# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 17:06:44 2018
script to run the status and trends data aggregation tool
https://data.ca.gov/dataset/water-quality-data
@author: jsaracen
"""
from fetch import fetch_data_files
from read import read_data_files
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
        for name, df in data.items():
            try:
                print('Storing {} to database'.format(name.lower()))
                df.to_sql(name, engine, if_exists="append")
            except:
                print('Couldn''t store  {} to database'.format(name))
                pass
    except psycopg2.OperationalError:
        print("Couldnt connect to database, make sure its running and try again")
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
        store_data(data)    
    return data

if __name__ == "__main__":
    data = main(store=False)