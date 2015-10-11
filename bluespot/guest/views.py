from flask import Blueprint,render_template,jsonify,request,current_app,abort,redirect,url_for
from functools import wraps
from sqlalchemy import and_,or_
import uuid
from functools import wraps
from facebook import get_user_from_cookie, GraphAPI
from unifi.controller import Controller
import datetime
import random
from .models import Guest,Device,Guestsession,Guesttrack,Facebookauth
from .const import *
from .forms import FacebookTrackForm,generate_emailform
from bluespot.extensions import db
from bluespot.base.utils.helper import format_url
from bluespot.base.utils.forms import print_errors,get_errors


bp = Blueprint('guest', __name__,template_folder='templates')



@bp.route('/')
def client_index( ):
    #return render_template('user/login.html')
    abort(404)

@bp.route('/s/<site_id>/',methods = ['GET', 'POST'])
def guest_portal(site_id):

    #--get all URL parameters, expected URL format--
    device_mac = request.args.get('id')
    ap_mac   = request.args.get('ap')   
    orig_url = request.args.get('url')   
  
    if not device_mac or not ap_mac:
        current_app.logger.error("Guest portal called with empty ap_mac/user_mac")
        abort(404)
    guest_device = None
    #create guest tracking entry
    track_id = str(uuid.uuid4())
    guest_track = Guesttrack(ap_mac=ap_mac,device_mac=device_mac,state=GUESTRACK_INIT,orig_url=orig_url,track_id=track_id)
    db.session.add(guest_track)
    #Initialize the session, check if the user has recently logged in 
    guest_session = Guestsession.query.filter( and_(Guestsession.mac==device_mac,Guestsession.state != SESSION_EXPIRED)).first() 
    #Check if the device was ever logged
    guest_device =  Device.query.filter(Device.mac==device_mac).first()
    if not guest_session:
        #create session
        guest_session = Guestsession(mac=device_mac,state=SESSION_INIT)
        db.session.add(guest_session)
        #check for guest device
        if guest_device:
            #device was logged once, add session to the device      
            guest_device.sessions.append(guest_session)
        else:
            #device was never logged, create a new device and add a session
            guest_device = Device(mac=device_mac,state=DEVICE_INIT)
            db.session.add(guest_device)
            guest_device.sessions.append(guest_session)
        db.session.commit()
    #session exists
    else:
        if not guest_device:
            current_app.logger.error("Guest Session exists, but Device not found in DB!! MAC:%s AP:%s"%(device_mac,ap_mac))
            abort(404)    
    #connect this session to our guest track entry
    guest_track.session = guest_session
    guest_session.guesttracks.append(guest_track)
    guest_track.state = GUESTRACK_SESSION
    db.session.commit()    
    if current_app.config['LANDINGSITE']['loginmethod'] ==1:
        #AUTH mode is set to social
        return redirect(url_for('guest.social_login',track_id=guest_track.track_id),code=302)        
    elif current_app.config['LANDINGSITE']['loginmethod'] ==2:
        #AUTH mode is set to social
        return redirect(url_for('guest.email_login',track_id=guest_track.track_id),code=302)   

   
@bp.route('/auth/guest/<track_id>')
def authorize_guest(track_id):
    '''Function called after respective auth mechanisms are completed
    
       This function send API commands to controller, redirect user to correct URL
    '''
    
    #
    #Validate track id and get all the needed variables
    guest_track = Guesttrack.query.filter_by(track_id=track_id).first()
    if not guest_track:
        current_app.logger.error("Called authorize_guest with wrong track ID:%s"%track_id)
        abort(404)
        
    #validate session associated with this track ID
    guest_session = Guestsession.query.filter_by(id=guest_track.session_id).first()
    if not guest_session:
        current_app.logger.error("Called authorize_guest with wrong Session from track ID:%s"%track_id)
        abort(404)   


    #Check if the session is authorized
    if not guest_session.state == SESSION_AUTHORIZED:
        current_app.logger.error("Called authorize_guest with wrong Non Authorized session with track ID:%s"%track_id)
        abort(404) 

    #Send  unifi API commands if the user has completed login
    if not current_app.config['NO_UNIFI'] :
        #code to send auth command to controller
        try:
            c =  Controller(current_app.config['LANDINGSITE']['unifihost'], current_app.config['LANDINGSITE']['unifiadmin'], current_app.config['LANDINGSITE']['unifipass'],current_app.config['LANDINGSITE']['unifiport'],current_app.config['LANDINGSITE']['unifiversion'],current_app.config['LANDINGSITE']['unifisiteid'])       
            c.authorize_guest(guest_track.device_mac,guest_session.duration,ap_mac=guest_track.ap_mac)    
        except:
            current_app.logger.exception('Exception occured while trying to authorize User')
            return "Error Occured!"
    
    #Code to handle guest after successful login 
    
    if current_app.config['LANDINGSITE']['redirecturl']:
        return redirect(format_url(current_app.config['LANDINGSITE']['redirecturl']))
    elif guest_track.orig_url is not None:
        #redirect User's URL
        return redirect(format_url(guest_track.orig_url))
    else:
        #redirect user to google.com
        return redirect(format_url("www.google.com"),code=302)

@bp.route('/tempauth/guest/<track_id>')
def temp_authorize_guest(track_id):
    '''Function for giving temporary internet access for a client
    
       This function send API commands to controller, return ok
    '''
    guest_track = Guesttrack.query.filter_by(track_id=track_id).first()
    if not guest_track:
        current_app.logger.error("Called temp_authorize_guest with wrong track ID:%s"%track_id)
        abort(404)
        
    #validate session associated with this track ID
    guest_session = Guestsession.query.filter_by(id=guest_track.session_id).first()
    if not guest_session:
        current_app.logger.error("Called temp_authorize_guest with wrong Session from track ID:%s"%track_id)
        abort(404)   
    guest_track.state =GUESTRACK_TEMP_AUTH
    db.session.commit()

    #get details from track ID and authorize
    if not current_app.config['NO_UNIFI'] :
        try:
            c =  Controller(current_app.config['LANDINGSITE']['unifihost'], current_app.config['LANDINGSITE']['unifiadmin'], current_app.config['LANDINGSITE']['unifipass'],current_app.config['LANDINGSITE']['unifiport'],current_app.config['LANDINGSITE']['unifiversion'],current_app.config['LANDINGSITE']['unifisiteid'])       
            c.authorize_guest(guest_track.device_mac,5,ap_mac=guest_track.ap_mac)    
        except:
            current_app.logger.exception('Exception occured while trying to authorize User')
            return jsonify({'status':0,'msg': "Error!!"})
        return jsonify({'status':1,'msg': "DONE"})
    else:
        return jsonify({'status':1,'msg': "DEBUG enabled"})

@bp.route('/social/guest/<track_id>',methods = ['GET', 'POST'])
def social_login(track_id):
    ''' Function to called if the site is configured with Social login    
    
    '''
    #
    #Validate track id and get all the needed variables
    guest_track = Guesttrack.query.filter_by(track_id=track_id).first()
    if not guest_track:
        current_app.logger.error("Called social_login with wrong track ID:%s"%track_id)
        abort(404)
        
    #validate session associated with this track ID
    guest_session   = Guestsession.query.filter_by(id=guest_track.session_id).first()
    guest_device    = Device.query.filter_by(id=guest_session.device_id).first()
  
    if not guest_session or not guest_device :
        current_app.logger.error("Called social_login with wrong Session/Device/Wifisite from track ID:%s"%track_id)
        abort(404) 
    #
    #Check if the device already has a valid auth
    if  guest_device.state == DEVICE_AUTH:
        #Device has a guest element and is authorized
        guest_session.state = SESSION_AUTHORIZED
        guest_track.state   = GUESTRACK_SOCIAL_PREAUTH
        guest_device.state  = DEVICE_AUTH
        db.session.commit()
        #redirect to authorize_guest
        return redirect(url_for('guest.authorize_guest',track_id=guest_track.track_id),code=302)
    else:
        #show the configured landing page
        
        return get_landing_page(app_id=current_app.config['LANDINGSITE']['fbappid'],track_id=track_id )

@bp.route('/facebook/check/<track_id>',methods = ['GET', 'POST'])
def facebook_login(track_id):
    ''' Function to called if the site is configured for advanced facebook authentication.
    
    '''
    #fbtrackform = FacebookTrackForm()
    auth_like = None
    auth_post = None
    #if fbtrackform.validate_on_submit():
    if request.method == 'POST':
        auth_like = request.form['authlike']
        auth_post = request.form['authpost']
    # Attempt to get the short term access token for the current user.
    check_user_auth = get_user_from_cookie(cookies=request.cookies, app_id=current_app.config['LANDINGSITE']['fbappid'],app_secret=current_app.config['LANDINGSITE']['fbappsecret'])
    current_app.logger.debug("APPID:%s Secret:%s"%(current_app.config['LANDINGSITE']['fbappid'],current_app.config['LANDINGSITE']['fbappsecret']))
    if not check_user_auth or not check_user_auth['uid']:
        #
        #User is not logged into DB app, redirect to social login page
        print check_user_auth

        return redirect(url_for('guest.social_login',track_id=track_id),code=302)
    #Validate track id and get all the needed variables
    guest_track = Guesttrack.query.filter_by(track_id=track_id).first()
    if not guest_track:
        current_app.logger.error("Called authorize_guest with wrong track ID:%s"%track_id)
        abort(404)
        
    #validate session associated with this track ID
    guest_session   = Guestsession.query.filter_by(id=guest_track.session_id).first()
    guest_device    = Device.query.filter_by(id=guest_session.device_id).first()
  
    if not guest_session or not guest_device:
        current_app.logger.error("Called authorize_guest with wrong Session/Device/Wifisite from track ID:%s"%track_id)
        abort(404) 


    #check this FB profile already added into our DB,else add it
    profile_check = Facebookauth.query.filter_by(profile_id=check_user_auth['uid']).first()
    if not profile_check:
        profile_check = Facebookauth()
        profile_check.profile_id    = check_user_auth['uid']
        profile_check.token         = check_user_auth['access_token']
        db.session.add(profile_check)
        db.session.commit
        
    #profile already added to DB, check if the user had already authorized the site
    guest_check = Guest.query.filter(Guest.fb_profile==profile_check.id).first()
    if not guest_check:
        #Guest entry for this user is not available in DB,add the same.
        try:
            graph = GraphAPI(check_user_auth['access_token'])
            profile = graph.get_object(profile_check.profile_id)
        except:
            #Exception while calling graph API, redirect user to same page to try again
            current_app.logger.exception("Exception while calling FB API")
            return redirect(url_for('guest.facebook_login',track_id=track_id),code=302)
        else:
            guest_check = Guest()
            guest_check.firstname    = profile.get('first_name')
            guest_check.lastname    = profile.get('last_name')
            guest_check.email   = profile.get('email')
            guest_check.facebookauth = profile_check           
            profile_check.guests.append(guest_check)
            db.session.add(guest_check)
            db.session.commit()
    #
    if current_app.config['LANDINGSITE']['enablefblike'] == 1:
        current_app.logger.debug("Current value of authlike:%s authpost:%s"%(auth_like,auth_post))
        if guest_track.fb_liked !=1:
            if guest_check.fb_liked:
                # if the guest has liked the page already, mark guesttrack as liked
                current_app.logger.debug("Guest with ID:%s had already liked page"%guest_check.id )
                guest_track.fb_liked = 1
                db.session.commit()
            elif auth_like == '1' :
                #quick hack to test for liking and posting, guest has skipped the liking, allow
                #internet for now and ask next time
                current_app.logger.debug("Guest with ID:%s Track ID:%s Decided to skip liking landing page "%(guest_check.id,guest_track.id) )
                guest_track.fb_liked = 1
                db.session.commit()
            elif auth_like == '2':
                #user has liked the page mark track and guest as liked
                current_app.logger.debug("Guest with ID:%s Track ID:%s Has liked landing page "%(guest_check.id,guest_track.id) )
                guest_track.fb_liked = 1
                guest_check.fb_liked = 1
                db.session.commit()
            else:
                # show page asking user to like
                current_app.logger.debug("Guest with ID:%s Track ID:%s is new, show the FB landing page "%(guest_check.id,guest_track.id) )
                landing_page = current_app.config['LANDINGPAGE']
                return render_template("fb/like.html",clientpage = landing_page,app_id=current_app.config['LANDINGSITE']['fbappid'],track_id=track_id,fb_page=current_app.config['LANDINGSITE']['fbpageurl'])


    #mark sessions as authorized
    guest_session.state = SESSION_AUTHORIZED
    guest_track.state   = GUESTRACK_NEW_AUTH
    guest_device.guest  = guest_check
    guest_check.devices.append(guest_device)
    if guest_check.fb_liked == 1 : # if guest has full filled all the social login criterias,mark the device as authed
        guest_device.state  = DEVICE_AUTH
    db.session.commit()
    return redirect(url_for('guest.authorize_guest',track_id=guest_track.track_id),code=302)
    

@bp.route('/email/guest/<track_id>',methods = ['GET', 'POST'])
def email_login(track_id):
    ''' Function to called if the site is configured with Social login    
    
    '''
    #
    #Validate track id and get all the needed variables
    guest_track = Guesttrack.query.filter_by(track_id=track_id).first()
    if not guest_track:
        current_app.logger.error("Called social_login with wrong track ID:%s"%track_id)
        abort(404)
        
    #validate session associated with this track ID
    guest_session   = Guestsession.query.filter_by(id=guest_track.session_id).first()
    guest_device    = Device.query.filter_by(id=guest_session.device_id).first()
  
    if not guest_session or not guest_device :
        current_app.logger.error("Called social_login with wrong Session/Device/Wifisite from track ID:%s"%track_id)
        abort(404) 
    #
    #Check if the device already has a valid auth
    if  guest_device.state == DEVICE_AUTH:
        #Device has a guest element and is authorized
        guest_session.state = SESSION_AUTHORIZED
        guest_track.state   = GUESTRACK_SOCIAL_PREAUTH
        guest_device.state  = DEVICE_AUTH
        db.session.commit()
        #redirect to authorize_guest
        return redirect(url_for('guest.authorize_guest',track_id=guest_track.track_id),code=302)
    else:
        #show the configured landing page
        email_form = generate_emailform(current_app.config['LANDINGSITE']['formfields'])

        if email_form.validate_on_submit():
            newguest = Guest()
            newguest.populate_from_email_form(email_form,current_app.config['LANDINGSITE']['formfields'])
            db.session.add(newguest)
            db.session.commit()
            #mark sessions as authorized
            guest_session.state = SESSION_AUTHORIZED
            guest_track.state   = GUESTRACK_NEW_AUTH
            guest_device.guest  = newguest
            newguest.devices.append(guest_device)
            guest_device.state  = DEVICE_AUTH
            db.session.commit()
            return redirect(url_for('guest.authorize_guest',track_id=guest_track.track_id),code=302)
        
        return get_landing_page(track_id=track_id,email_form=email_form)

def get_landing_page(landing_page=None,**kwargs):
    ''' Function to return configured landing page for a particular site    

    '''
    landing_site = ''
    landing_page = current_app.config['LANDINGPAGE']
    if current_app.config['LANDINGSITE']['loginmethod'] ==1 :
        return render_template('social_landing.html',landing_site=landing_site,clientpage=landing_page,**kwargs)
    elif current_app.config['LANDINGSITE']['loginmethod'] ==2 :
        return render_template('email_landing.html',landing_site=landing_site,clientpage=landing_page,**kwargs)
        
