"""OAuth utils:

* urlencode

* urldecode

* generating SHA1 signatures
"""

import urllib

import hashlib
from hashlib import sha1
import hmac
import base64

def normalize_parameters(param):
    """Normalizes the param(eter) dictionary (with properties: key and value)
    resulting in a sorted string that is urlencoded
    """

    param = sorted(
            param, 
            key = lambda item : u"%s %s" % (item['key'],
            item['value'])
        )

    return_string = ''

    for item in param:
        if len(return_string):
            return_string += "&"
        return_string += urlencode_RFC3986(
                item['key']) + '=' + urlencode_RFC3986(item['value'])
    return return_string

def normalize_key_value_parameters(param):
    """Normalizes a dict, returns a urlencoded string
    """
    param_array = []
    
    for key, value in param.items():
        param_array.append({'key':key, 'value':value})
    
    return normalize_parameters(param_array)
    
def urlencode_RFC3986(value):
    """Urlencode a string.
    
    .. note::
         some characters are not encoded or encoded different from python's
         default (such as the ~, the space is converted to %20 
         instead of a +)
    """
    return urllib.quote_plus(str(value)).replace('%7E', '~').replace('+', '%20')
    
def urlencode_RFC3986_unicode(value):
    """Unicode version of urlencode_RFC3986"""
    return unicode(urlencode_RFC3986(value))
    
def urldecode_RFC3986(value):
    """ decode a string"""
    return urllib.unquote_plus(value)
    
def urldecode_RFC3986_unicode(value):
    """ unicode decode a string"""
    return unicode(urldecode_RFC3986(value))
    
def generate_base_string(http_method, uri, params):
    """ Generates urlencoded string from the method, uri and params parameters
    """
    base_string = [
        urlencode_RFC3986_unicode(http_method),
        urlencode_RFC3986_unicode(uri),
        urlencode_RFC3986_unicode(params),
    ]
    
    return u"&".join(base_string)
    
def calculate_hmacsha1_signature(base_string, consumer_secret, token_secret):
    """ Generate the signature based on the secrets and the base string
    """
    key = [
        urlencode_RFC3986_unicode(consumer_secret),
        urlencode_RFC3986_unicode(token_secret),
    ]
    
    key = u"&".join(key)
    
    return base64.b64encode(hmac_sha1(str(key), str(base_string )))
    
def hmac_sha1(key, text):
    """ Return the sha1 signature
    """
    return hmac.new(key, text, sha1).digest()
