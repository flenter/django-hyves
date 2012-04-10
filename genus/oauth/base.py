"""
Module containing the OAuth base class
"""
class OAuthBase(object):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
