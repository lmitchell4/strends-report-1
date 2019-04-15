
# basic sqlalchemy libs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import config


# load config and credentials from ini file
engine_args = config('sqlalchemy_database.ini')
#file should return the following
engine_args = {'db_type': 'postgresql',
               'host': 'localhost',
               'database': 'DBNAME',
               'user': 'USERNAME',
               'password': 'PASSWORD',
               'port': '5432'}
# build connection string load
connection_string = "{db_type}://{user}:{password}@{host}:{port}/{database}".format(**engine_args)
engine = create_engine(connection_string )
# create a session connection to that db
Session = sessionmaker(bind=engine)
# Ceate a new base class from which all mapped classes should inherit
Base = declarative_base(engine)
