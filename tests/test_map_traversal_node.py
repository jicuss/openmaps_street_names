import unittest

import mock
from lib.map_traversal.map_traversal_node import MapTraversalNode
from lib.overpass.overpass_api import OverpassAPI
from lib.overpass.overpass_api_cache import OverpassAPICache

class MapTraversalNodeTests(unittest.TestCase):
    def setUp(self):
        self.mock_cache = mock.create_autospec(OverpassAPICache)
        self.mock_api = mock.create_autospec(OverpassAPI)

        self.coordinates = [1,2,3,4]
        self.node = MapTraversalNode(self.coordinates,self.mock_api,self.mock_cache)

    def tearDown(self):
        pass

    def test_coordinates(self):
        self.assertEquals(self.node.coordinates(),[1,2,3,4])

    def test_fragment_key(self):
        self.assertEquals(self.node.fragment_key(),'coordinate_1.0_2.0_3.0_4.0')
        pass

    # @mock.patch('lib.string_functions.query_statements.box_query_residential',side_effect=['FakeQuery'])
    @mock.patch('lib.map_traversal.map_traversal_node.box_query_residential',side_effect=['FakeQuery'])
    def test_process_fragment_doesnt_exist(self,mock_query):
        self.mock_cache.cache_fragment_exists.return_value = False
        self.node.process()
        self.mock_api.query_api.assert_called_with('FakeQuery',self.node.fragment_key())
        self.assertEquals(self.node.processed,True)
        pass

    # todo rework this, remove calls to the fragment exist method (only for testing)

    def test_process_fragment_does_exist(self):
        self.mock_cache.cache_fragment_exists.return_value = True
        self.node.process()
        self.mock_api.query_api.assert_not_called()
        self.assertEquals(self.node.processed,True)
        pass


    def test_process_fragment_already_processed(self):
        self.node.processed = True
        self.node.process()
        self.mock_api.query_api.assert_not_called()
        self.mock_cache.cache_fragment_exists.assert_not_called()
        pass

if __name__ == '__main__':
    unittest.main()
