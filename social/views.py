"""
Basic authentication for hyves using the genus API
"""
import pickle


from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import mail_admins

from django.contrib.sites.models import Site
from django.contrib.auth import authenticate, login

from social.models import UserAssociation
from social.signals import social_user_authenticated
from social.decorators import accesstoken_required, requesttoken_required
from genus.oauth.consumer import OAuthConsumer
from genus.api import GenusApi

from social.utils import get_genus

def index(request, show_more = False):
    """Retrieve the index... currently also does a small API call
    """
    
    if request.GET.get('logintoken'):
        return redirect(
            reverse(
                'social.views.get_authorization_by_logintoken',
                kwargs = {
                    'logintoken':request.GET.get('logintoken')
                    }
            ) + "?%s" % request.META['QUERY_STRING']
        )
    context = {}
    
    if show_more:
        genus = get_genus()
        
        result = genus.do_method(
            "media.getPublic",
            {
                "sorttype":"mostrespect",
                'mediatype':'image',
                'timespan':'day'
            }
        )
        
        context.update({'media': result['media']})
    
    return render_to_response('social/index.html', context)
    
def get_authorization_by_logintoken(request, logintoken):
    """Redirect for users who do have a logintoken (i.e. a hyvertysing page)
    """
    genus = get_genus()
    
    access_token = genus.retrieve_access_token_by_login(
        logintoken
    )
    
    access_token, created = UserAssociation.objects.get_or_create_from_token(
            access_token
        )
    
    user = authenticate(
        username = access_token.user.username,
        password = access_token.get_password())
    
    if not user:
        mail_admins(
            'authenticate failure for: %s ' % access_token.user.username,
            'Faulty password? or user does not exist')
        
    login(request, user)
    
    social_user_authenticated.send(
        sender = None,
        user = user,
        access_token = access_token)
    
    return HttpResponseRedirect(reverse('get_authorized') + "?%s" % request.META['QUERY_STRING'])
    
def get_user_authorization(request):
    """Redirects to the hyves page to ask for permission
    """
    from django.conf import settings
    consumer = OAuthConsumer(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    
    genus = GenusApi(consumer, "2.0")
    
    token = genus.retrieve_request_token(settings.CONSUMER_METHODS, "default")
    request.session['requesttoken_user'] = pickle.dumps(token)
    import sys
    try:
        site = Site.objects.get_current()
    
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    print 
    url = genus.get_authorize_url(
    token,
    "http://" + site.domain + reverse('authorized_redirect')
    )
        
        
    return HttpResponseRedirect(url)
    #return render_to_response('social/index.html', context)


@requesttoken_required
def get_user_authorized_popup(request, genus = None, requesttoken_user = None):
    """Should open a popup.. unfortunately, this is not yet tested
    """
    token = requesttoken_user
    
    access_token = genus.retrieve_access_token(token)
    
    access_token, created = UserAssociation.objects.get_or_create_from_token(
            access_token
        )
    
    authenticate(username = access_token.user.username, nopass = True)
    
    context = {}
    
    return render_to_response('social/popup.html', context)
    
@requesttoken_required
def get_user_authorized_redirect(
        request, genus = None,
        requesttoken_user = None):
    """User has authorized, so store the access token and redirect to a more
    useful page
    """
    token = requesttoken_user
    
    access_token = genus.retrieve_access_token(token)
    userid = access_token.userid
    
    access_token, created = UserAssociation.objects.get_or_create_from_token(
            access_token
        )
    
    user = authenticate(
        username = access_token.user.username,
        password = access_token.get_password())
    
    if not user:
        mail_admins(
            'authenticate failure for: %s ' % access_token.user.username,
            'Faulty password? or user does not exist')
        
    login(request, user)
    
    social_user_authenticated.send(
        sender = None,
        user = user,
        access_token = access_token)
    
    return HttpResponseRedirect(reverse('get_authorized'))
    

@accesstoken_required
def get_authorized(
        request,
        genus = None,
        requesttoken_user = None,
        access_token = None
    ):
    """User is authorized, show generic overview
    """
    
    context = {
    }
    
    return render_to_response(
        (
            'customcore/authorized.html',
            'social/authorized.html',
        ),
        context,
    )
    

    
def get_invalid_session(request):
    """You should not be here: this is an error page. Should be used
    when a user is not logged in etc..
    """

    mail_admins(
       'invalid session',
       'An attempt to make an api based call was done without being logged in as a valid user.\n\
        The user\'s name was: %s\n\
        And the URL: %s\n\
        with paramters: %s' % ( request.user, request.path_info, request.GET.urlencode())
    )
    
    return render_to_response('social/invalid_session.html', {})

@accesstoken_required
def do_method(request, method, genus = None, access_token = None):
    """Make an api call with method @param method
    """
    
    params = {}
    
    if(method == "users.getFriendsByLoggedinSorted"):
        params.update(
            {
                'sorttype': 'alphabetically',
                'ha_responsefields': 'profilepicture',
                'ha_resultsperpage': 2,
            }
        )
        
    response = genus.do_method(method, params, access_token)
    
    return render_to_response('social/authorized.html', {'result':response})
    
