"""
Module containing a small OAuth AccessToken subclass
"""

from base import OAuthBase
from datetime import datetime

class OAuthAccessToken(OAuthBase):
    """Small OAuth access token 
    """

    methods = []
    expiredate = datetime.now
    def __init__(self, key, secret, userid):
        super(OAuthAccessToken, self).__init__(key, secret)

        self.userid = userid
        #self.methods = methods
        #self.expiredate = expiredate
