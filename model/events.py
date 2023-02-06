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
class Event(db.Model):
    __tablename__ = 'events'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    #_uid = db.Column(db.String(255), unique=True, nullable=False)
    _email = db.Column(db.String(255), unique=False, nullable=False)
    _event_name = db.Column(db.String(255), unique=False, nullable=False)
    _event_details = db.Column(db.String(255), unique=False, nullable=False)
    _date = db.Column(db.String(255), unique=False, nullable=False)
    _start_time = db.Column(db.String(255), unique=False, nullable=False)
    _end_time = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self) 
    def __init__(self, name, email, event_name, event_details, date, start_time, end_time):
        self._name = name
        self._email = email
        self._event_name = event_name
        self._event_details = event_details
        self._date = date
        self._start_time = start_time
        self._end_time = end_time
    
    #here's the name getter
    @property
    def name(self):
        return self._name

    #here's the name setter
    @name.setter
    def name(self, name):
        self._name = name
    
    #here's the email getter
    @property
    def email(self):
        return self._email
    
    #here's the email setter
    @email.setter
    def email(self, email):
        self._email = email
    
    #here's the event_name getter
    @property
    def event_name(self):
        return self._event_name
    
    #here's the event_name setter
    @event_name.setter
    def event_name(self, event_name):
        self._event_name = event_name
    
    #here's the event_details getter
    @property
    def event_details(self):
        return self._event_details
    
    #here's the event_details setter
    @event_details.setter
    def event_details(self, event_details):
        self._event_details = event_details
    
    #here's the date getter
    @property
    def date(self):
        return self._date
    
    #here's the date setter
    @date.setter
    def date(self, date):
        self._date = date

    #here's the start_time getter
    @property
    def start_time(self):
        return self._start_time
    
    #here's the start_time setter
    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    #here's the end_time getter
    @property
    def end_time(self):
        return self._end_time
    
    #here's the end_time setter
    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time
    
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
            "email": self.email,
            "event_name": self.event_name,
            "event_details": self.event_details,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", email="", event_name="", event_details="", date="", start_time="", end_time=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(email) > 0:
            self.email = email
        if len(event_name) > 0:
            self.event_name = event_name
        if len(event_details) > 0:
            self.event_details = event_details
        if len(date) > 0:
            self.date = date
        if len(start_time) > 0:
            self.start_time = start_time
        if len(end_time) > 0:
            self.end_time = end_time
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
def initEvents():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    e1 = Event(name="Thomas Edison", email="tedison@lightbulb.edu",
        event_name="The Edison Troupe Meet",
        event_details="We 10 selected geniuses will meet in the events room for a convergence.",
        date="02/23/2023", start_time="13:00", end_time="14:00")
    e2 = Event(name="John Mortensen", email="jmortensen@powayusd.com",
        event_name="Extra Credit Code Meetup",
        event_details="Come to work on ideation and any confusion with the Full Stack CPT project. No phones.",
        date="02/25/2023", start_time="10:00", end_time="12:00")
    e3 = Event(name="Karl Giant", email="giantrichguy@wallstreet.org",
        event_name="Karl and Cats",
        event_details="Karl would like to see cats with friends (if he can fit in the building).",
        date="02/26/2023", start_time="16:00", end_time="17:00")
    
    events = [e1, e2, e3]

    """Builds sample events data"""
    for event in events:
        try:
            event.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {event.event_name}")