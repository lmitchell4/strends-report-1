
# basic sqlalchemy libs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# connect to the containerized db
engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
# create a session connection to that db
Session = sessionmaker(bind=engine)

Base = declarative_base()