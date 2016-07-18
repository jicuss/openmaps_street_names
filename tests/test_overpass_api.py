import unittest

import mock
import overpy
from lib.overpass.overpass_api_cache import OverpassAPICache

from lib.overpass.overpass_api import OverpassAPI


class OverpassAPITests(unittest.TestCase):
    def setUp(self):
        self.mock_cache = mock.create_autospec(OverpassAPICache)
        self.mock_overpi = mock.create_autospec(overpy.Overpass)
        self.api = OverpassAPI(self.mock_overpi, self.mock_cache)

    def tearDown(self):
        ''

    def test_query_api_if_in_cache(self):
        ''' If the fragment key is found to be in the cache, don't query the API just return what's in the cache '''
        self.mock_cache.cache_fragment_exists.return_value = True
        self.mock_cache.load_cache_fragment.return_value = 'example_response'

        self.assertEquals(self.api.query_api('example_request', 'fragment_key'), 'example_response')
        self.mock_overpi.query.assert_not_called()

    def test_query_api_if_not_in_cache(self):
        '''
            If the fragment key is found not to be in the cache, query the API. Store response in the cache
            For simplicity, no nodes or ways will be returned by the mock API query.
        '''
        self.mock_cache.cache_fragment_exists.return_value = False
        self.mock_overpi.query('').nodes.return_value = []
        self.mock_overpi.query('').ways.return_value = []

        self.api.query_api('example_request', 'fragment_key')
        self.mock_overpi.query.assert_called_with('example_request')
        self.mock_cache.store_cache_fragment.assert_called_with('fragment_key', {'nodes': [], 'ways': []})

    def test_failed_query_api_call(self):
        '''
            Test what happens is the query API raises a OverpassTooManyRequests exception? It should sleep for 90 seconds.
        '''
        pass

if __name__ == '__main__':
    unittest.main()
