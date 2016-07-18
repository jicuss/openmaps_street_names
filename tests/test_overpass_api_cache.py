import unittest
import mock
from lib.overpass.overpass_api_cache import OverpassAPICache

class OverpassAPICacheTests(unittest.TestCase):
    def setUp(self):
        self.cache = OverpassAPICache()
        self.cache.cache_path = '/data/cache/'

    @mock.patch('lib.overpass.overpass_api_cache.os')
    def test_establish_directory_structure(self, mock_os):
        mock_os.path.exists.return_value = False
        self.cache.establish_directory_structure()
        mock_os.makedirs.assert_called_with('/data/cache/')

    def test_fragment_cache_path(self):
        self.assertEquals(self.cache.fragment_cache_path('fragment_key'),'/data/cache/fragment_key')

    @mock.patch('lib.overpass.overpass_api_cache.os')
    def test_cache_fragment_exists(self,mock_os):
        mock_os.path.exists.return_value = True
        self.assertTrue(self.cache.cache_fragment_exists('something'))
        mock_os.path.exists.return_value = False
        self.assertFalse(self.cache.cache_fragment_exists('something'))

    @mock.patch('lib.overpass.overpass_api_cache.os')
    def test_clear_cache_fragment(self,mock_os):
        mock_os.path.exists.return_value = True
        self.cache.fragment_cache_path = mock.Mock(return_value='/data/cache/fragment_name')
        self.cache.clear_cache_fragment('fragment_name')
        mock_os.remove.assert_called_with('/data/cache/fragment_name')

    def test_store_cache_fragment(self):
        # todo. figure out how to mock out the file access
        self.cache = OverpassAPICache('cache_test')
        self.cache.store_cache_fragment('test_fragment',{"key": "value"})

    def test_load_cache_fragment(self):
        # todo. figure out how to mock out the file access
        self.cache = OverpassAPICache('cache_test')
        self.assertEquals(self.cache.load_cache_fragment('test_fragment'),{"key": "value"})

if __name__ == '__main__':
    unittest.main()
