# coding=utf-8

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import Base


class ManagementArea(Base):
    __tablename__ = 'management_areas'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    area_sq_mi = Column(Integer)

    def __init__(self, name, area_sq_mi):
      self.name = name
      self.area_sq_mi = area_sq_mi