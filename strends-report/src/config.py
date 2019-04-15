# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 12:27:33 2019

@author: jsaracen
.ini file stores credentials and looks like this:

[postgresql]
host=localhost
database=DBNAME
user=USER
password=PASSWORD
port=5432

"""

from configparser import ConfigParser
 
 
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db