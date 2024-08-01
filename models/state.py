#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class

    Attributes:
        __tablename__ (str): MySQL's table name to store states
        name (str): state's name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City", backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            get the list of City instances with
            state_id aquals to the current State.id
            """
            my_cities = []
            all_instances = list(models.storage.all(City).values())
            for city in all_instances:
                if city.state_id == self.id:
                    my_cities.append(city)
            return my_cities
