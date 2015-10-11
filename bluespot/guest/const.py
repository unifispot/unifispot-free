SESSION_INIT            = 1
SESSION_AUTHORIZED      = 3
SESSION_EXPIRED         = 4
SESSION_BAN             = 5

GUESTRACK_INIT          = 1 #Guesttrack creation
GUESTRACK_SESSION       = 2 #guesttrack is assigned a session
GUESTRACK_NO_AUTH       = 3 #guest track of no_auth site
GUESTRACK_TEMP_AUTH     = 4 #guesttrack authorization started
GUESTRACK_NEW_AUTH      = 5 #newly authorized guest track
GUESTRACK_SOCIAL_PREAUTH= 6 #guesttrack devices previously authorized

DEVICE_INIT             = 1
DEVICE_AUTH             = 2
DEVICE_SMS_AUTH         = 3
DEVICE_BAN              = 4

GUEST_INIT              = 1
GUEST_AUTHORIZED        = 2
GUEST_BANNED            = 3



form_fields_dict = { 'firstname':"Firstname",'lastname':'Last Name','email':'Email ID','phonenumber':'Phone Number'}
