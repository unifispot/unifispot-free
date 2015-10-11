# Unifispot

Unifispot is an external captive portal for Unifi Controllers that supports details collection and Facebook login
It is built using python and flask and runs on apache/nginx or any webserver that supports wsgi.


Requirements
============
1. Apache 2
2. WSGI module
3. Python 2.7+

Installation
============

Ubuntu
------
I have created .deb packages for Ubuntu 32/64 bit systems. Which can be installed using dpkg tools 

Packages are available in http://download.unifispot.com/ubuntu/


Installation From Source
-------------------
1. Clone git repository to your machine.
2. Install all the dependencies.  
(pip -r requirements.txt)
3. Initilize Database by executing rebuild.sh
4. Deploy the application using wsgi. Reffer to http://flask.pocoo.org/docs/0.10/deploying/ for more details.
   Example configurations can be found in unifispot.conf and unifispot.wsgi



Configuration
=============
Portal can be configured fully by modifying config.yaml file available in the root directory

Config file has two parts named LANDINGSITE and LANDING PAGE

LANDINSITE: Represents various parameters to be configured for selecting authentication mechanism,facebook APP ID etc

LANDINGPAGE:Defines the look and feel of landing page such as colors/fonts etc.


Viewing the LandingPage
=======================
If the instalaltion is successfull you can view the landing page by going to http://192.168.1.1/guest/s/site?id=11:22:33:44:55:66&ap=22:33:44:55:66:77

Admin Area For Viewing Guest Details
=======================
Portal also has a password protected dashboard area for viewing the details entered by the guest.
Username and password can be configured in config.yaml. The default username and password will be admin/password

Admin Area: http://192.168.1.1/admin



