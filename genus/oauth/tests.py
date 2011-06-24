import unittest

from utils import normalize_key_value_parameters

class OAuthUtilsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_normalize_key_value(self):
        #print '!'
        self.assertEqual(normalize_key_value_parameters({'test':'tset'}), 'test=tset')
        self.assertEqual(normalize_key_value_parameters({'test':'a', 'atest':'2'}), 'atest=2&test=a')
        self.assertEqual(normalize_key_value_parameters({'test':'dit is een test'}), 'test=dit%20is%20een%20test')
        self.assertEqual(normalize_key_value_parameters({'test':'dit+is+een+test'}), 'test=dit%2Bis%2Been%2Btest')

if __name__ == '__main__':
    unittest.main()