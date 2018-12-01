# coding=utf-8

# 1 - imports
from salmon import Salmon
from base import Session
from management_area import ManagementArea

# 2 - extract a session
session = Session()

salmons = session.query(Salmon).all()

def Average(lst): 
    return sum(s.length for s in lst) / len(lst)

average_size = Average(salmons)
print('### Average len of Salmon (inches):')
print(f'{average_size} inches')
print('')

management_areas = session.query(ManagementArea) \
    .filter(ManagementArea.area_sq_mi > 4000) \
    .all()

print('### Management areas with size over 1000 sq. mi')
for area in management_areas:
    print(f'{area.name} is {area.area_sq_mi}')
print('')

