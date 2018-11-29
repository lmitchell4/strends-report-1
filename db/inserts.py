# coding=utf-8
from datetime import date

# import all the tables and the base schema
from base import Session, engine, Base
# from salmon import Salmon
# from management_area import ManagementArea

from movie import Movie
from actor import Actor
from contact_details import ContactDetails
from stuntman import Stuntman

# generate db schema
Base.metadata.create_all(engine)

session = Session()

print('connected to DB')

# 4 - create movies
bourne_identity = Movie("The Bourne Identity", date(2002, 10, 11))
furious_7 = Movie("Furious 7", date(2015, 4, 2))
pain_and_gain = Movie("Pain & Gain", date(2013, 8, 23))

# 5 - creates actors
matt_damon = Actor("Matt Damon", date(1970, 10, 8))
dwayne_johnson = Actor("Dwayne Johnson", date(1972, 5, 2))
mark_wahlberg = Actor("Mark Wahlberg", date(1971, 6, 5))

# 6 - add actors to movies
bourne_identity.actors = [matt_damon]
furious_7.actors = [dwayne_johnson]
pain_and_gain.actors = [dwayne_johnson, mark_wahlberg]

# 7 - add contact details to actors
matt_contact = ContactDetails("415 555 2671", "Burbank, CA", matt_damon)
dwayne_contact = ContactDetails("423 555 5623", "Glendale, CA", dwayne_johnson)
dwayne_contact_2 = ContactDetails("421 444 2323", "West Hollywood, CA", dwayne_johnson)
mark_contact = ContactDetails("421 333 9428", "Glendale, CA", mark_wahlberg)

# 8 - create stuntmen
matt_stuntman = Stuntman("John Doe", True, matt_damon)
dwayne_stuntman = Stuntman("John Roe", True, dwayne_johnson)
mark_stuntman = Stuntman("Richard Roe", True, mark_wahlberg)

# 9 - persists data
session.add(bourne_identity)
session.add(furious_7)
session.add(pain_and_gain)

session.add(matt_contact)
session.add(dwayne_contact)
session.add(dwayne_contact_2)
session.add(mark_contact)

session.add(matt_stuntman)
session.add(dwayne_stuntman)
session.add(mark_stuntman)

# chinook_river = ManagementArea("Chinook River", 7298) # basic management area has a name and square mileage
# fish1 = Salmon("Salmon", "Chinook", 79, False, 16, "male", True, date(2016, 4, 2))
# fish1.management_area = chinook_river
# # session.add(chinook_river) # not needed because sqlalchemy will cascade the save-update
# session.add(fish1)

print('sessions finished, records added')

session.commit()
session.close()