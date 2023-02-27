from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import *

from model.wordles import Wordle
from model.wordles import deleteID


wordle_api = Blueprint('wordle_api', __name__,
                   url_prefix='/api/wordles')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(wordle_api)

class WordleAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''

            # validate name
            name = body.get('name')
            if name is None or len(name) < 1:
                return {'message': f'Name is missing, or is less than 1 character'}, 210
            # validate pin
            pin = body.get('pin')
            if pin is None or len(pin) < 2:
                return {'message': f'Pin is missing, or is less than 2 characters'}, 220
            #validate score
            score = body.get('score')
            if score=="" or int(score)<1 or int(score)>6:
                return {'message': f'Score is missing, or is not within range (1-6, inclusive).'}, 230

            ''' #1: Key code block, setup USER OBJECT '''
            wo = Wordle(name=name, 
                      score=score,
                      pin=pin)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            wordle = wo.create()
            # success returns json of user
            if wordle:
                return jsonify(wordle.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or name {name} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            wordles = Wordle.query.all()    # read/extract all users from database
            json_ready = [wordle.read() for wordle in wordles]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class _Delete(Resource):
        def delete(self):
            body = request.get_json()
            user_id = body.get('id')
            user_pin = body.get('pin')
           
            #status = deleteID(user_id)
            status = deleteID(user_id, user_pin)
            if status:
                return {'message': f'Successfully deleted user with id {user_id} '}
            else:
                return {'message': f'User with id {user_id} not found'}, 240

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Delete, '/delete')

