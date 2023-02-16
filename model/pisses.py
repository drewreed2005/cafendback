""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Piss(db.Model):
    __tablename__ = 'pisses'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=False)
    _level = db.Column(db.String(255), unique=False, nullable=False)
    _time = db.Column(db.String(255), unique=False, nullable=False)
    _pin = db.Column(db.String(255), unique=True, nullable=False)


    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, level, time, pin):
        self._name = name    # variables with self prefix become part of the object, 
        self._level = level
        self._time = time
        self._pin = pin

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts level from object
    @property
    def level(self):
        return self._level
    
    # a setter function, allows name to be updated after initial object creation
    @level.setter
    def level(self, level):
        self._level = level
    
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, time):
        self._time = time
    
    @property
    def pin(self):
        return self._pin

    @pin.setter
    def pin(self, pin):
        self._pin = pin
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "time": self.time,
            "pin": self.pin,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", level="", time="", pin=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(level) > 0:
            self.level = level
        if len(time) > 0:
            self.time = time
        if len(pin) > 0:
            self.pin = pin
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initPisses():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = Piss(name='Thomas Edison', level='100', time='00:03:01', pin='aspoi')
    u2 = Piss(name='Nicholas Tesla', level='200', time='00:10:13', pin='brian')
    u3 = Piss(name='Alexander Graham Bell', level='123', time='00:07:20', pin='23451')
    u4 = Piss(name='Eli Whitney', level='432', time='00:06:09', pin='who')
    u5 = Piss(name='John Mortensen', level='340', time='10:16:21', pin='apcs')

    pisses = [u1, u2, u3, u4, u5]

    """Builds sample user/note(s) data"""
    for piss in pisses:
        try:
            piss.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate level, or error: {piss.pin}")
            