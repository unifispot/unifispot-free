import os
from passlib.hash import sha256_crypt

#WTF
CSRF_ENABLED = True


#configure blue prints 

BLUEPRINTS = ('guest','admin')



#Configure DB
basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','bluespot')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = 'once-a-cat-went-to-talk'


SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)),'database.db')
SECURITY_PASSWORD_HASH = 'sha256_crypt'
SECURITY_PASSWORD_SALT = "AJSHASJHAJSHASJHSAJHASJAHSJAHJSA"



#SQLALCHEMY_ECHO = True
STATIC_FILES = os.path.join(basedir,'static')

#SQLALCHEMY_ECHO = True
ASSETS_DEBUG = True 
DEBUG = False

UNIFI_HOST = '127.0.0.1'
UNIFI_USER = 'ubnt'
UNIFI_PASS = 'ubnt'
UNIFI_VERSION = 'v4'
UNIFI_PORT = '8443'
UNIFI_SITE_ID ='default'

FB_APP_ID = ''
FB_APP_NAME = 'bluespot'
FB_APP_SECRET = ''


NO_UNIFI = False

