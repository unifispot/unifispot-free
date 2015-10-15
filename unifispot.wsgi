import os
import sys


path = os.path.join(os.path.dirname(__file__), os.pardir)
if path not in sys.path:
    sys.path.append(path)
this_dir = os.path.dirname(__file__)
sys.path.insert(0, this_dir)

# The application object is used by any WSGI server configured to use this
# file.


from bluespot import create_app
application = create_app(mode= 'development')

import logging
from logging.handlers import RotatingFileHandler
log_file = '/var/www/unifispot/production.log'
file_handler = RotatingFileHandler(log_file,'a', 1 * 1024 * 1024, 10)
application.logger.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
application.logger.addHandler(file_handler)