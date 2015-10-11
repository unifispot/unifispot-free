from functools import wraps
from flask import request, Response,Blueprint,render_template,jsonify,current_app,abort,redirect,url_for

from bluespot.extensions import db
from bluespot.base.utils.helper import format_url
from bluespot.base.utils.forms import print_errors,get_errors
from bluespot.guest.models import Guest

bp = Blueprint('admin', __name__,template_folder='templates')


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    if username == current_app.config['LANDINGSITE']['adminusername'] and password == current_app.config['LANDINGSITE']['adminpassword'] :
        return 1
    else:
        return None

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@bp.route('/')
@requires_auth
def client_index( ):
    items = Guest.query.filter_by().all()
    return render_template('admin/dashboard.html',items=items)
    



