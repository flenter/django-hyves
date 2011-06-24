from base import OAuthBase

class OAuthAccessToken(OAuthBase):
    
    def __init__(self, key, secret, userid, methods, expiredate):
        
        super(OAuthAccessToken, self).__init__(key, secret)
        
        self.userid = userid
        self.methods = methods
        self.expiredate = expiredate
        
