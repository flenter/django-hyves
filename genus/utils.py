"""Small library of util methods
"""

import urllib
from urllib import FancyURLopener

from oauth.utils import normalize_key_value_parameters, generate_base_string, \
                        calculate_hmacsha1_signature


def do_http_call(url, variables, do_post):
    """Make the HTTP call.
    Note exceptions can be raised should the HTTP status require it.
    """
    if type(variables) != str:
        variables = urllib.urlencode(variables)
        
    opener = FancyURLopener()
    
    if(do_post):
        fhandle = opener.open(url, variables)
    else:
        url_call = url + '?' + variables
        
        fhandle = opener.open(url_call)
        
    result = fhandle.read()
    
    fhandle.close()
    
    return result

def bool_to_string(bool):
    """Converts a boolean to string (all lowercase)"""
    if bool:
        return 'true'
    return 'false'
    
def string_to_bool(text):
    """Converts a string to a boolean (not case sensitive).
    
    .. note::
       only the value true (not case sensitive) results in a boolean value
       True. All other values result in a False"""
    if text.lower() == 'true':
        return True
    return False

def calculate_oauth_signature(
        http_method,
        uri,
        variables,
        consumer_secret,
        token_secret):
    """Calculates the oauth signature"""
    params = normalize_key_value_parameters(variables)
    base_string = generate_base_string(http_method, uri, params)
    return calculate_hmacsha1_signature(
        base_string,
        consumer_secret,
        token_secret
    )
