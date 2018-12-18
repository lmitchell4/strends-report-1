# coding=utf-8
from datetime import date

# import all the tables and the base schema
from base import Session, engine, Base
from salmon import Salmon
from management_area import ManagementArea

# generate db schema
Base.metadata.create_all(engine)

session = Session()

print('connected to DB')

chinook_river = ManagementArea("Chinook River", 7298) # basic management area has a name and square mileage
session.add(chinook_river)

fish1 = Salmon("Salmon", "Chinook", 79, False, 16, "male", True, date(2016, 4, 2))
fish1.management_area = chinook_river

session.add(fish1)

print('session finished, records added')

session.commit()
session.close()