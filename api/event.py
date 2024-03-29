from flask import Flask, Blueprint, request, jsonify
from flask_restful import Api, Resource #restful building
from datetime import *
from flask_cors import CORS

from model.events import Event, deleteID

event_api = Blueprint('event_api', __name__,
                   url_prefix='/api/events')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(event_api)

class EventAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Submitter\'s name is missing, or is less than 2 characters'}, 210
            # validate uid
            email = body.get('email')
            if email is None or len(email) < 2:
                return {'message': f'Email is missing, or is less than 2 characters'}, 210
            # look for the rest of the data
            event_name = body.get('event_name')
            event_details = body.get('event_details')
            date = body.get('date')
            if (date is None) or (len(date) != 10) or (int(date[6:10]) < 2023) or (int(date[6:10]) > 2024):
                return {'message': f'Date is missing, formatted incorrectly, or within an invalid time range.'}, 210
            start_time = body.get('start_time')
            end_time = body.get('end_time')
            password = body.get('password')

            ''' #1: Key code block, setup USER OBJECT '''
            eo = Event(name=name, 
                      email=email,
                      event_name=event_name,
                      event_details=event_details,
                      date=date,
                      start_time=start_time,
                      end_time=end_time,
                      password=password)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            event = eo.create()
            # success returns json of user
            if event:
                return jsonify(event.read())
            # failure returns error
            return {'message': f'Processed {event_name}, either a format error or the event "{event_name}" is a duplicate'}, 210

    class _Read(Resource):
        def get(self):
            events = Event.query.all()    # read/extract all users from database
            json_ready = [event.read() for event in events]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class _Delete(Resource):
        def delete(self):
            body = request.get_json() #getting the database data for a given event
            event_id = body.get('id') #isolating the ID of the given entry
           
            status = deleteID(event_id) #uses the deleteID function from the model
            if status:
                return {'message': f'Successfully deleted event with id {event_id} '}
            else:
                return {'message': f'Event with id {event_id} not found'}, 240

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Delete, '/delete')