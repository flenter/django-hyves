from genus.api import GenusApi
from genus.oauth.consumer import OAuthConsumer

def get_genus():
    """creates an instance of the GenusAPI
    """
    
    from django.conf import settings
    
    consumer = OAuthConsumer(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    
    genus = GenusApi(consumer, "2.0")
    
    return genus


import sys
from random import Random

def generate_password(passwordLength=8, alternate_hands=True):
    """Generate a random password of passwordLength length and possibly with
    alternating characters for left/right hand
    """
    rng = Random()
    
    righthand = '23456qwertasdfgzxcvbQWERTASDFGZXCVB'
    lefthand = '789yuiophjknmYUIPHJKLNM'
    allchars = righthand + lefthand
    
    password = ""
    for i in range(passwordLength):
        if not alternate_hands:
            password += rng.choice(allchars)
        else:
            if i%2:
                password += rng.choice(lefthand)
            else:
                password += rng.choice(righthand)

    return password

