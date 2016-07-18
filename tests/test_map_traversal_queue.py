import unittest

import mock
from lib.map_traversal.map_traversal_node import MapTraversalNode
from lib.overpass.overpass_api import OverpassAPI
from lib.overpass.overpass_api_cache import OverpassAPICache

class MapTraversalQueueTests(unittest.TestCase):
    def setUp(self):
        self.mock_cache = mock.create_autospec(OverpassAPICache)
        self.mock_api = mock.create_autospec(OverpassAPI)

        self.coordinates = [1,2,3,4]
        self.node = MapTraversalNode(self.coordinates,self.mock_api,self.mock_cache)

    def tearDown(self):
        pass

    def test_coordinates(self):
        pass

if __name__ == '__main__':
    unittest.main()
