
from base import OAuthBase

class OAuthRequestToken(OAuthBase):
    def __init__(self, key, secret):
        super(OAuthRequestToken, self).__init__(key, secret)        
        