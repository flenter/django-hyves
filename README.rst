A port of the php library genus (http://code.google.com/p/genusapis/) for the (Dutch) social network site Hyves 

It consists of 3 parts:

1. genus, genus.oauth (namespace) the port of the library
2. social, a basic django implementation including some decorators who 
   are the projects equivolent of login_required
3. example, a small django project using this.

See the example project for all dependencies.

One important remark for people who want to integrate this with their own
projects or want to play with the example project::

 don't forget to create a hyves api consumer_key and secret. You also need 
 to do this for the example project.

Some more remarks for integrating the django enabled social part of this 
package with your own project:

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
