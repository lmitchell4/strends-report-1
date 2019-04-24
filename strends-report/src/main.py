# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 17:06:44 2018
script to run the status and trends data aggregation tool
https://data.ca.gov/dataset/water-quality-data
@author: jsaracen
"""

import io
import numpy as np
import os
import pickle
import sqlalchemy

from base import engine
from fetch import fetch_data_files
from read import read_data_files, write_postgresql_table_names
from setup_paths import FILE_PATHS_PATH,RESULTS_PATH

#TODO:* Create database schema
#TODO:* Add logging
#TODO:* Pass arguments from command line using argparse

def fetch_data():
    fetch_data_files()


def read_data(FILE_PATHS_FILENAME):
    return read_data_files(FILE_PATHS_FILENAME)


def df_str_cleanup(df):
    #To replace all line breaks in all textual columns b/c they return DataError  when loading 
    for col in df.columns: 
        if df[col].dtype == np.object_:
            df[col] = df[col].str.replace('\n','');
            df[col] = df[col].str.replace('\r','');
    return df


def to_postgresql(engine, df, table_name, if_exists='replace', sep='\t', encoding='utf8'):
    connection = None
    cursor = None
    # Create Table
    df[:0].to_sql(table_name, engine, if_exists=if_exists)
    try:
        df = df_str_cleanup(df)
    except (Exception, AttributeError) as error: # Workaround on table "ls_smelt": Repeat the string replace process to deal with a strange AttributeError
        print(error)
        df = df_str_cleanup(df)
    # Prepare data
    output = io.StringIO()
    df.to_csv(output, sep=sep, header=False, encoding=encoding)
    output.seek(0)
    # Insert data
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.copy_from(output, table_name, sep=sep, null='')
        connection.commit()
        print("Database successfully updated with table {}".format(table_name))
    except (Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print(error)
        print("Rolling back connection")
        connection.rollback()
        raise
    finally:  
        if connection is not None:
            connection.close() 
    return


def store_data(data):
    try:        
        print('Storing data to postgresSQL database...')
        for table_name, df in data.items():
            try:   
                print("Writing table {}".format(table_name))
                to_postgresql(engine, df, table_name)
            except sqlalchemy.exc.SQLAlchemyError :#catch a specific error  message 
                print('Could not store {} to database, check database connection {} and try again'.format(table_name.lower(),engine), engine)
    except (Exception, sqlalchemy.exc.OperationalError) as error: 
        print("Couldn''t connect to database, make sure its running and try again")#update message to match corresponding error
        print(error)
    except (Exception, sqlalchemy.exc.SQLAlchemyError) as error:
        print("There was an unknown generic sqlalchemy error")
        print(error)
    finally:
        print ("Database updated with current data")
    return


def main(store=False):
    """main entry point for the script"""
    # FILE_PATHS_FILENAME = "file_paths.json" 
    fetch_data()
    data = read_data(FILE_PATHS_PATH)    
    if store:
        write_postgresql_table_names(data)
        store_data(data)    
    return data


if __name__ == "__main__":
    #read the raw data and optionally store to the db
    store = True
    save_to_pickle = True
    data = main(store=store)
  #  if store2db == False:
        #save it to a pickle for later viewing instead of writing to the db
    if save_to_pickle:
        PICKLED_DATA_PATH = os.path.join(RESULTS_PATH, 'data.pickle')
        with open(PICKLED_DATA_PATH, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #load it from a pickle for qucik viewing
#        PICKLED_DATA_PATH = os.path.join(RESULTS_PATH, 'data.pickle')
#
#        
#        with open(PICKLED_DATA_PATH, 'rb') as handle:
#            data = pickle.load(handle)