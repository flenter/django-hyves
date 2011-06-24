import unittest

from genus.utils import bool_to_string, string_to_bool
from genus.utils import do_http_call
from genus.utils import calculate_oauth_signature

from genus.api import GenusApi

from genus.oauth.consumer import OAuthConsumer

class UtilsTestCase(unittest.TestCase):
    """Testing the utils library for any inconsistancies etc
    """
    
    def test_bool_conversion(self):
        """Testing the boolean to string conversions
        """
        
        self.assertEqual(bool_to_string(False), 'false')
        self.assertEqual(bool_to_string(True), 'true')
        
        self.assertEqual(string_to_bool('false'), False)
        self.assertEqual(string_to_bool('true'), True)
        
    def test_do_http_call(self):
        """Try to do an HTTP request
        """
        
        result = do_http_call(
            'http://youtube.com/crossdomain.xml',
            {
              'test':'value'
            },
            False
        )

        self.assertTrue(result.count('cross-domain-policy')>0)
    
    def test_calculate_signatures(self):
        """Calculate and compare signatures. Including the tricky situations
        """
        
        self.assertEqual(
            calculate_oauth_signature(
                'http://data.hyves.nl/',
                'uri',
                {
                    'test':'value'
                },
                'consumer_secret',
                'token_secret'
            ),
            'AD7pfDU3JJNsaXZW4uGccTt0Mj8='
        )
        
        self.assertEqual(
            calculate_oauth_signature(
                'POST',
                'TEST',
                {
                    'a':'b test'
                },
                'oauth_consumer_secret',
                'oauth_token_secret'),
            'HPcbjA9VIzxoQDRYGnOVWGpyMec='
        )
        
        self.assertEqual(
            calculate_oauth_signature(
                'POST',
                'TEST',
                {
                    'a':'b+&test'
                },
                'oauth_consumer_secret',
                'oauth_token_secret'
            ),
            '3pKzqGPLUmQ4jF5QuirKSQFyVtU='
        )
        

class GenusApiTestCase(unittest.TestCase):
    """Test case to see if an api call can really be made
    """
    
    CONSUMER_KEY = 'MzMwMl9JPo83Vt7DlywcI0hnOlAr'
    CONSUMER_SECRET = 'MzMwMl82a7r6P8VJhs4RNMrpGDeN'
    
    def setUp(self):
        self.consumer = OAuthConsumer(
            GenusApiTestCase.CONSUMER_KEY,
            GenusApiTestCase.CONSUMER_SECRET
        )
        
        self.genus_api = GenusApi(self.consumer, "2.0")
        
    def test_do_method(self):
        """Make an API call to the server.
        """
        response = self.genus_api.do_method(
            "media.getPublic",
            {
                "sorttype":"mostrespect",
                'mediatype':'image',
                'timespan':'day'
            }
        )
        
        self.assertTrue(len(respone) > 0)
        
if __name__ == '__main__':
    unittest.main()