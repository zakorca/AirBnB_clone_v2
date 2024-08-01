#!/usr/bin/python3
""" Defines a module to manage database storage using sqlAlchemy """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """ creates a database storage engine

    Attributes:
        __engine (sqlalchemy.engine): SQLAlchemy engine.
        __session (sqlalchemy.Session): SQLAlchemy session.
    """

    __engine = None
    __session = None
    __classes = [User, State, City, Amenity, Place, Review]

    def __init__(self):
        """Initialize instances attributes for dbStorage"""
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'
                .format(getenv("HBNB_MYSQL_USER"),
                        getenv("HBNB_MYSQL_PWD"),
                        getenv("HBNB_MYSQL_HOST"),
                        getenv("HBNB_MYSQL_DB")),
                pool_pre_ping=True)
        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session (self.__session)
        all objects depending of the class name
        """
        my_dict = {}
        if cls is None:
            for c in self.__classes:
                for obj in self.__session.query(c).all():
                    key = obj.__class__.__name__ + '.' + obj.id
                    my_dict[key] = obj
        else:
            if cls in self.__classes:
                for obj in self.__session.query(cls).all():
                    key = obj.__class__.__name__ + '.' + obj.id
                    my_dict[key] = obj
        return my_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ close the session """
        self.__session.close()
