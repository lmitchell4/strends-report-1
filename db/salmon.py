# coding=utf-8

from sqlalchemy import Boolean, Column, String, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

from base import Base

class Salmon(Base):
    __tablename__ = 'salmon'
    
    id = Column(Integer, primary_key=True)
    species_group = Column(String)
    species = Column(String)
    length = Column(Integer)
    eggs = Column(Boolean)
    age = Column(Integer)
    sex = Column(String)
    tagged = Column(Boolean)
    sample_date = Column(Date)
    management_area_id = Column(Integer, ForeignKey('management_area.id'))

    def __init__(self, species_group, species, length, eggs, age, sex, tagged, sample_date):
      self.species_group = species_group
      self.species = species
      self.length = length
      self.eggs = eggs
      self.age = age
      self.sex = sex
      self.tagged = tagged
      self.sample_date = sample_date