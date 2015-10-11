from bluespot.extensions import db
import datetime
import uuid


class Guest(db.Model):
    ''' Class to represent guest profile, it will be filled fully/partially depending upon site configuration

    '''
    id          = db.Column(db.Integer, primary_key=True)
    firstname   = db.Column(db.String(60))
    lastname    = db.Column(db.String(60))
    age         = db.Column(db.Integer,index=True)
    gender      = db.Column(db.Integer,index=True)
    state       = db.Column(db.Integer,index=True)
    email       = db.Column(db.String(60))
    phone       = db.Column(db.String(15))
    devices     = db.relationship('Device', backref='guest',lazy='dynamic')
    fb_profile  = db.Column(db.Integer, db.ForeignKey('facebookauth.id'))
    fb_liked    = db.Column(db.Integer)
    fb_posted   = db.Column(db.Integer)

    def populate_from_email_form(self,form,form_fields):
        for form_field in form_fields:
            val = getattr(form,form_field).data 
            setattr(self,form_field,val)


class Device(db.Model):
    ''' Class to represent guest's device, each guest can have multiple devices attached to his account

    '''
    id          = db.Column(db.Integer, primary_key=True)
    mac         = db.Column(db.String(30),index=True)
    hostname    = db.Column(db.String(60),index=True)
    state       = db.Column(db.Integer)
    guest_id    = db.Column(db.Integer, db.ForeignKey('guest.id'))
    sessions    = db.relationship('Guestsession', backref='device',lazy='dynamic')

class Guestsession(db.Model):
    ''' Class to represent guest session. Each session is associated to a Guest and will have a state associated with it.

    '''
    id          = db.Column(db.Integer, primary_key=True)
    device_id   = db.Column(db.Integer, db.ForeignKey('device.id'))
    starttime   = db.Column(db.DateTime,default=datetime.datetime.utcnow(),index=True)
    stoptime    = db.Column(db.DateTime,index=True)   #Time at which session is stopped, to be filled by session updator
    expiry      = db.Column(db.DateTime,index=True)   #predicted expiry time,default to 60 minutes
    temp_login  = db.Column(db.Integer,default=0)
    duration    = db.Column(db.Integer,default=60)
    ban_ends    = db.Column(db.DateTime,index=True)
    data_used   = db.Column(db.String(20))            #Data used up in this session
    state       = db.Column(db.Integer)
    mac         = db.Column(db.String(30),index=True)
    auth_code   = db.Column(db.String(20))            #Authorization code for this session, used for vouchers
    d_updated   = db.Column(db.String(20))            #data updated last
    duration    = db.Column(db.Integer)               #Duration in seconds the session lasted, updated by session updator   
    guesttracks = db.relationship('Guesttrack', backref='guestsession',lazy='dynamic')


class Guesttrack(db.Model):
    ''' Class to track connection attempts, this is also used to track login process

    '''
    id          = db.Column(db.Integer, primary_key=True)
    track_id    = db.Column(db.String(40),index=True,unique=True)
    session_id  = db.Column(db.Integer, db.ForeignKey('guestsession.id'))
    ap_mac      = db.Column(db.String(20),index=True)
    device_mac  = db.Column(db.String(20),index=True)
    timestamp   = db.Column(db.DateTime,default=datetime.datetime.utcnow(),index=True)
    state       = db.Column(db.Integer,index=True)
    fb_liked    = db.Column(db.Integer,index=True,default=0)
    fb_posted   = db.Column(db.Integer,index=True,default=0)
    orig_url    = db.Column(db.String(200))


class Facebookauth(db.Model):
    ''' Class to represent guest's Facebook connection, this is needed as one common APP is used for tracking guests in different sites.

    '''
    id          = db.Column(db.Integer, primary_key=True)
    profile_id  = db.Column(db.String(30), nullable=False,index=True)
    token       = db.Column(db.String(50), nullable=False)
    state       = db.Column(db.Integer)
    guests      = db.relationship('Guest', backref='facebookauth',lazy='dynamic')
    
