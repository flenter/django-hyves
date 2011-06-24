
from base import OAuthBase

class OAuthConsumer(OAuthBase):
    
    def __init__(self, key, secret):
        #super(OAuthBase, self).__init__(key, secret)
        self.key = key
        self.secret = secret