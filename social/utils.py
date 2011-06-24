from genus.api import GenusApi
from genus.oauth.consumer import OAuthConsumer

def get_genus():
    """creates an instance of the GenusAPI
    """
    
    from django.conf import settings
    
    consumer = OAuthConsumer(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    
    genus = GenusApi(consumer, "2.0")
    
    return genus
