""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Wordle(db.Model):
    __tablename__ = 'wordles'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _pin = db.Column(db.String(255), unique=False, nullable=False)
    #_uid = db.Column(db.String(255), unique=True, nullable=False)
    _score = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self) 
    def __init__(self, name, score, pin):
        self._name = name
        self._pin = pin
        self._score = score
    
    #here's the name getter
    @property
    def name(self):
        return self._name

    #here's the name setter
    @name.setter
    def name(self, name):
        self._name = name
    
    #here's the pin getter
    @property
    def pin(self):
        return self._pin
    
    @pin.setter
    def pin(self, pin):
        self._pin = pin
    
    #here's the score getter
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, score):
        self._score = score

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
            "pin": self.pin,
            "score": self.score
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", pin="", score=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(pin) > 0:
            self.pin = score
        if len(score) > 0:
            self.score = score
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
def initWordles():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = Wordle(name="Thomas Edison", score=12, pin="qwerty123")
        u2 = Wordle(name="John Mortensen", score=15, pin="codec0decod3bro")
        u3 = Wordle(name="Karl Giant", score=10, pin="i_am-the-f4th3r")
        
        wordles = [u1, u2, u3]
        #Builds sample wordles data
        for wordle in wordles:
            try:
                wordle.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate data, or error: {wordle.name}")
