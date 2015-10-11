#! flask/bin/python
from os.path import abspath

from flask import current_app
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets
from flask.ext.migrate import Migrate, MigrateCommand

from bluespot import create_app
from bluespot.extensions import db


app = create_app(mode='development')
manager = Manager(app)
manager.add_command('assets', ManageAssets())
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

manager.run()
#app.run(host='0.0.0.0',debug = True)
