# -*- coding: utf-8 -*-
# based on example from https://github.com/danbruegge/flaskeleton/blob/master/app/base/utils/core.py
import logging
from logging.handlers import SMTPHandler
from werkzeug.utils import import_string
# from werkzeug.utils import ImportStringError


def load_blueprints(app, blueprint_config='BLUEPRINTS',
                    blueprint_path='app', blueprint_name='bp'):
    """A simple blueprint loader, you only need to pass the app context and set
    a BLUEPRINTS constant with the a list of bluleprint names in the
    settings.py::

        BLUEPRINTS = ('blueprint1', 'blueprint2', )
    """

    for name in app.config[blueprint_config]:
        bp = import_string(
            '{0}.{1}.{2}'.format(blueprint_path, name, blueprint_name)
        )
        app.register_blueprint(
            bp,
            url_prefix=app.config[name.upper() + '_URL_PREFIX']
        )

    return app


def load_blueprint_settings(app, blueprint_config='BLUEPRINTS',
                            blueprint_path='app', blueprint_name='bp'):
    """A simple blueprint settings loader, you only need to pass the app
    context and set a BLUEPRINTS constant with the a list of bluleprint names
    in the settings.py::

        BLUEPRINTS = ('blueprint1', 'blueprint2', )
    """

    for name in app.config[blueprint_config]:
        # load a settings file for the blueprint
        app.config.from_object('{0}.{1}.settings'.format(blueprint_path, name))

    return app


def error_handler(app):
    """Seperated to keep the `create_app()` clean.
        Onely pass the app context and set the rights variables::

        ERROR_MAIL = {
            'smtp': '<SMTP SERVER',
            'to': ['<TO>'],
            'from': '<FROM>',
            'subject': '<SUBJECT>'
        }
    """

    mail_handler = SMTPHandler(app.config['ERROR_MAIL']['smtp'],
                               app.config['ERROR_MAIL']['to'],
                               app.config['ERROR_MAIL']['from'],
                               app.config['ERROR_MAIL']['subject'])
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

