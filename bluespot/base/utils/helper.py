from functools import wraps
from flask import redirect,url_for,abort,current_app,request
from flask.ext.security import current_user

from datetime import datetime,date, timedelta
import time 

#Add http to the URL if not already there
def format_url(url):
	if not url.startswith('http') or not url.startswith('https'):
		newurl =  '%s%s' % ('http://', url)
		return newurl
	return url
    


def client_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated():
            current_app.logger.debug("Client URL :%s called by a user not logged in"%request.url)
            return redirect(url_for('security.login', next=request.url))
        if not current_user.check_client():
            current_app.logger.debug("Client URL :%s called by a userID :%s who is not a client "%(request.url,current_user.id))
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated():
            current_app.logger.debug("Admin URL :%s called by a user not logged in"%request.url)
            return redirect(url_for('security.login', next=request.url))
        if not current_user.check_admin():
            current_app.logger.debug("Admin URL :%s called by a userID :%s who is not an admin "%(request.url,current_user.id))
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function    
    
def register_api(bp,view,endpoint,url,security_wrap):
    ''' Register API views for a serveradmin element'''
    view_func = security_wrap(view.as_view(endpoint))
    bp.add_url_rule(url, defaults={'id': None},
                     view_func=view_func, methods=['GET',])
    bp.add_url_rule(url, defaults={'id': None}, view_func=view_func, methods=['POST',])
    bp.add_url_rule(url+'<int:id>', view_func=view_func,methods=['GET', 'POST', 'DELETE'])

def pretty_date(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = 'just now'

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default

def get_dates_between(start_date,end_date):
    '''Returns dates in between given datetime objects

    '''
    delta = end_date - start_date
    return [start_date + timedelta(days=x)  for x in range(delta.days + 1)]






 