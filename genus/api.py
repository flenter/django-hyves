"""
Generic API module. This is the core logic for any Hyves communication
"""
import time
import random
import sys

import json
import logging

from genus import utils
from genus.oauth import utils as oauth_util

from genus.oauth.requesttoken import OAuthRequestToken
from genus.oauth.accesstoken import OAuthAccessToken


from genus.exceptions import GenusTransportError


class GenusApi():
    """Main class instance of the genus API port. 
    """

    DEFAULT_HA_FORMAT = 'json'
    DEFAULT_HA_FANCYLAYOUT = 'false'
    DEFAULT_OAUTH_SIGNATURE_METHOD = "HMAC-SHA1"
    HTTP_TYPE_GET = 'GET'
    HTTP_TYPE_POST = 'POST'
    API_URL = 'http://data.hyves-api.nl/'
    AUTHORIZE_URL = 'http://www.hyves.nl/api/authorize/'
    logger = logging.getLogger('genus.api')

    def __init__(self, consumer, ha_version):
        """Instantiate the GenusApi class. requires a OAuthConsumer
        """
        self.consumer = consumer
        self.ha_version = ha_version

        self.nonce = None
        self.timestamp_last_method = None

    def do_method(self,
                  ha_method,
                  params,
                  token = None,
                  http_type = HTTP_TYPE_POST):
        """Makes the hyves API call, raises exceptions over bad HTTP status
        codes and Hyves errors
        """

        default_params = {
            'oauth_consumer_key': self.consumer.key,
            'oauth_timestamp': self.get_oauth_timestamp(),
            'oauth_nonce': self.get_oauth_nonce(),
            'oauth_signature_method': GenusApi.DEFAULT_OAUTH_SIGNATURE_METHOD,
            'ha_method': ha_method,
            'ha_format': GenusApi.DEFAULT_HA_FORMAT,
            'ha_fancylayout': GenusApi.DEFAULT_HA_FANCYLAYOUT,
            'ha_version': self.ha_version,
        }

        oauth_consumer_secret = self.consumer.secret
        oauth_token_secret = ''

        if token:
            default_params['oauth_token'] = token.key
            oauth_token_secret = token.secret

        params.update(default_params)
        params['oauth_signature'] = utils.calculate_oauth_signature(
            http_type,
            GenusApi.API_URL,
            params,
            oauth_consumer_secret,
            oauth_token_secret)

        params = oauth_util.normalize_key_value_parameters(params)

        try:
            response = utils.do_http_call(
                GenusApi.API_URL,
                params,
                http_type == GenusApi.HTTP_TYPE_POST
            )

        except IOError, exception:
            self.logger.exception(exception)

        json_response = json.loads(response)

        json_response = check_for_errors(json_response)

        return json_response

    def do_batch_methods(
            self,
            methods = None,
            token = None,
            http_type = HTTP_TYPE_POST):
        """Requires an array of methods.
        Each method is an object with the following properties:
        * params
        * ha_method

        Requires the 'batch.process' API call to be available
        """

        data = []

        for method in methods:
            default_params = {
                    'ha_method': method['ha_method'],
                    'ha_fancylayout': GenusApi.DEFAULT_HA_FANCYLAYOUT,
                    'ha_format': GenusApi.DEFAULT_HA_FORMAT,
                    'ha_version': self.ha_version
            }
            params = method['params']
            params.update(default_params)

            data.append(oauth_util.normalize_key_value_parameters(params))

        return self.do_method(
            'batch.process',
            {
                    'request': ','.join(data)
            },
            token,
            http_type
        )

    def retrieve_request_token(self, methods, expiration_type = 'default'):
        """Makes the api call 'auth.requesttoken'

        .. note::
            values for expiration_type can be found in the Hyves API
            documentation
        """
        response = self.do_method(
            "auth.requesttoken",
            {
                'methods': ','.join(methods),
                'expirationtype':expiration_type
            }
        )

        return OAuthRequestToken(
            response['oauth_token'],
            response['oauth_token_secret']
        )

    def retrieve_access_token(self, oauth_request_token):
        """Make the API call to retrieve an accesstoken
        Object returned is an OAuthAccessToken
        """
        response = self.do_method("auth.accesstoken", {}, oauth_request_token)

        token = OAuthAccessToken(
                response['oauth_token'],
                response['oauth_token_secret'],
                response['userid'],
                )

        token.methods = response['methods']
        token.expiredate = response['expiredate']

        return token

    def retrieve_access_token_by_login(self, token):
        """Get a nice oauth token based on a logintoken
        """
        response = self.do_method(
            'auth.accesstokenByLogintoken',
            {
                'logintoken': token,
            }
        )

        token = OAuthAccessToken(
            response['oauth_token'],
            response['oauth_token_secret'],
            response['userid'],
        )

        token.methods = response['methods']
        token.expiredate = response['expiredate']

        return token

    def get_oauth_timestamp(self):
        """Generate an oauth timestamp.
        This should be equal or more than the previous timestamp
        """
        timestamp = int(time.time())

        if self.timestamp_last_method == timestamp:
            self.nonce += 1
        else:
            self.timestamp_last_method = timestamp
            self.nonce = 0

        return self.timestamp_last_method

    def get_oauth_nonce(self):
        """returns a new nonce
        This value should be unique to prevent any replay attacks
        """
        ip_address = '127.0.0.1'
        rand = random.randint(0, sys.maxint -1)

        return str(self.nonce) + "_" + ip_address + "_" + str(rand)


def check_for_errors(response):
    """Check the response of the hyves API call
    """
    if response.has_key('error_code'):

        error_code = response.get('error_code')

        method = 'unknown'
        for parameter in response['request_parameters']['parameter']:
            if parameter['requestkey'] == 'ha_method':
                method = parameter['requestvalue']

        error_code = response['error_code']

        raise GenusTransportError(method, error_code)

    return response

def get_authorize_url(oauth_request_token, callback = None):
    """Returns the url to authorize the user (based on the
    GenusAPI.AUTHORIZE_URL)
    """
    url = GenusApi.AUTHORIZE_URL + "?oauth_token=" + oauth_request_token.key

    if callback:
        url += "&oauth_callback=" + oauth_util.urlencode_RFC3986(callback)

    return url
