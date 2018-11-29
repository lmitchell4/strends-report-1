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
upper_klamath = ManagementArea("Upper Klamath River", 3217) # basic management area has a name and square mileage
session.add(upper_klamath)

fish1 = Salmon("Salmon", "Chinook", 79, False, 16, "male", True, date(2016, 4, 2))
fish1.management_area = chinook_river

fish2 = Salmon("Salmon", "Sockeye", 88, True, 19, "female", True, date(2016, 5, 1))
fish2.management_area = upper_klamath

session.add(fish1)
session.add(fish2)

print('session finished, records added')

session.commit()
session.close()