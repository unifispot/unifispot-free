from flask import render_template,redirect,url_for

from flask.ext.assets import Environment
import re

#import basic utlities
from base.utils.core import (load_blueprint_settings, load_blueprints,	    error_handler,)


#import bundles
from assets import bundles


import os
import yaml

from flask import Flask as BaseFlask, Config as BaseConfig

class Config(BaseConfig):
    """Flask config enhanced with a `from_yaml` method."""
    
    def from_yaml(self, config_file):
       
        with open(config_file) as f:
            c = yaml.load(f)
          
        for key in c.iterkeys():
            if key.isupper():
                self[key] = c[key]
                #print key

                
class Flask(BaseFlask):
    """Extended version of `Flask` that implements custom config class"""
    
    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)

def create_app(mode="development"):
    """Create webapp instance."""
    app = Flask(__name__)
    #Initilise DB
    from bluespot.extensions import db
    db.init_app(app)
    # Load the default configuration
    app.config.from_object('config.default')
    #Load user specified config
    app.config.from_yaml(os.path.join(app.root_path,'..','config.yaml'))
    #initlize assets
    assets = Environment(app)
    assets.register(bundles)    
    # simple load all blueprint settings, enabled in config
    load_blueprint_settings(app,blueprint_path='bluespot')
    # simple load all blueprints, enabled in config
    load_blueprints(app,blueprint_path='bluespot')
    # Enable DebugToolbar on debug
    # Enable error handler on productive mode
    if app.config['DEBUG']:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)
        app.logger.error( "DEV")

    else:
        # add errorhandler
        #error_handler(app)
        app.logger.error( "PROD")


    @app.route("/")
    def home():
        return "OK"

    return app


def remove_db_session(exception=None):
    db_session.remove()
