from flask.ext.wtf import Form
from wtforms import TextField, HiddenField
from wtforms.validators import Required,DataRequired,Email

from .const import form_fields_dict

class FacebookTrackForm(Form):

    authlike = HiddenField("Auth Like")
    authpost = HiddenField("Auth Post")

def generate_emailform(form_fields):
    class F(Form):
        pass
    for key in form_fields:
        if key in ['firstname','lastname','email','phonenumber']:
            if  key == 'email':
                setattr(F, key, TextField(form_fields_dict[key],validators =[DataRequired(),Email()]))
            else:
                setattr(F, key, TextField(form_fields_dict[key],validators = [Required()]))        

    return F()