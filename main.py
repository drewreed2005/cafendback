import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app,db  # Definitions initialization
from model.events import initEvents
from model.pisses import initPisses
from model.wordles import initWordles

# setup APIs
from api.piss import piss_api # Blueprint import api definition
from api.event import event_api
from api.wordle import wordle_api

# register URIs
app.register_blueprint(piss_api) # register api routes
app.register_blueprint(event_api)
app.register_blueprint(wordle_api) # register api routes

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.before_first_request
def activate_job():
    db.init_app(app)
    initEvents()
    initPisses()
    initWordles()

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    
    app.run(debug=True, host="0.0.0.0", port="8239")
