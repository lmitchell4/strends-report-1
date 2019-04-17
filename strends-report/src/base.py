import os
# basic sqlalchemy libs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config_db import config


# load config and credentials
path, fl = os.path.split(os.path.realpath(__file__)) #TODO: fix this with abs path to config dir
dbconfigfile =  os.path.join(path,'config','sqlalchemy_database.ini')
engine_args = config(dbconfigfile)
# build connection string load
connection_string = "{db_type}://{user}:{password}@{host}:{port}/{database}".format(**engine_args)
engine = create_engine(connection_string )
# create a session connection to that db
Session = sessionmaker(bind=engine)
# Ceate a new base class from which all mapped classes should inherit
Base = declarative_base(engine)
