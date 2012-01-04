============
Introduction
============


A port of the php library genus (http://code.google.com/p/genusapis/) for the (Dutch) social network site Hyves 

It consists of 3 parts:

1. genus, genus.oauth (namespace) the port of the library
2. social, a basic django implementation including some decorators who 
   are the projects equivolent of login_required
3. example, a small django project using this.

One important remark for people who want to integrate this with their own
projects or want to play with the example project::

    don't forget to create a hyves api consumer_key and secret. You also need 
    to do this for the example project.


-------------------
The example project
-------------------


To play with the example, install the additional packages as specified in the conf/requirements.txt file
(i.e. run ``pip install -r conf/requirements.txt``). Make sure you have an api key and modify the settings 
file accordingly. Look in the settings file for CONSUMER_KEY and CONSUMER_SECRET. Next, set CONSUMER_METHODS
to the right values. This works slightly different if you are a campaign on hyves site and your site is called 
with a special request token, in that case, hyves will determine the methods you will have access to.
After this only three more steps need to be taken:

1. run ``python manage.py syncdb``
2. run ``python manage.py migrate``
3. run ``python manage.py runserver`` and you are up and running.

One more thing, please set current site to the right domain in via the django admin.


----
Tips
----


Some tips for integrating the django enabled social part of this package with 
your own project:

- check the urls.py of the example project. The urls are sometimes named and 
  code is referring to those names (for reverse lookup purposes), so make sure
  you don't change the names
- add FLOW_REDIRECT_URL to your settings file
- add CONSUMER_METHODS to your settings file as an array of strings. This will 
  be used when loging in without a hyves generated logintoken (the flow you 
  probably will have when you are not running in an iframe).

Note:
 the flow with a popup enabled authorization is not fully tested (since 
 we never had the need for it).
