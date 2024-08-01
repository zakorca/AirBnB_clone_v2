#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey


class Review(BaseModel, Base):
    """ Review class to store review information
    Attributes:
        __tablename__ (str): MySQL's table name to store reviews
        place_id (String): review's place_id
        user_id (String): review's user_id
        text (String): review's description
    """
    __tablename__ = "reviews"
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    text = Column(String(1024), nullable=False)
