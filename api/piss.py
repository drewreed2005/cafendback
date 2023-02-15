from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
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
            points = body.get('points')
            if points is None or len(points) < 1:
                return {'message': f'Points is missing, or is less than 2 characters'}, 210
            time = body.get('time')
            if time is None or len(time) < 0:
                return {'message': f'Time is missing, or is less than 0 characters'}, 210
            pin = body.get('pin')
            if pin is None or len(pin) < 2:
                return {'message': f'Pin is missing, or is less than 2 characters'}, 210

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, 
                      points=points,
                      time=time,
                      pin=pin)
            
            ''' Additional garbage error checking '''
            # set password if provided
            
            # convert to date type
            
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or Pin {pin} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')