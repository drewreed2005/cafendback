from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.pisses import Piss

piss_api = Blueprint('piss_api', __name__,
                   url_prefix='/api/pisses')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(piss_api)

class PissAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            level = body.get('level')
            if level is None or len(level) < 1:
                return {'message': f'level is missing, or is less than 2 characters'}, 210
            time = body.get('time')
            if time is None or len(time) < 0:
                return {'message': f'Time is missing, or is less than 0 characters'}, 210
            pin = body.get('pin')
            if pin is None or len(pin) < 2:
                return {'message': f'Pin is missing, or is less than 2 characters'}, 210

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Piss(name=name, 
                      level=level,
                      time=time,
                      pin=pin)
            
            ''' Additional garbage error checking '''
            # set password if provided
            
            # convert to date type
            
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            piss = uo.create()
            # success returns json of user
            if piss:
                return jsonify(piss.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or Pin {pin} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            pisses = Piss.query.all()    # read/extract all users from database
            json_ready = [piss.read() for piss in pisses]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')