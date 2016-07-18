import unittest

import mock
from lib.map_traversal.map_traversal_node import MapTraversalNode
from lib.map_traversal.map_traversal_queue import MapTraversalQueue
from lib.overpass.overpass_api import OverpassAPI
from lib.overpass.overpass_api_cache import OverpassAPICache

class MapTraversalQueueTests(unittest.TestCase):
    def setUp(self):
        self.mock_cache = mock.create_autospec(OverpassAPICache)
        self.mock_api = mock.create_autospec(OverpassAPI)

        self.coordinates = [1,1,3,3] # establishes a lat long box that is expected to have 4 total nodes
        self.queue = MapTraversalQueue(self.coordinates,self.mock_api,self.mock_cache)

    def tearDown(self):
        pass

    def test_traversal_lat_long_bounds(self):
        '''
            Upon instantiation the queue should have been propagated with 4 nodes
        '''
        node_coordinates = reduce(lambda x,y: x + [y.coordinates()],self.queue.nodes,[])
        node_coordinates.sort()
        self.assertEquals(node_coordinates,[[1.0, 1.0, 2.0, 2.0], [1.0, 2.0, 2.0, 3.0], [2.0, 1.0, 3.0, 2.0], [2.0, 2.0, 3.0, 3.0]])

    def test_traversal_lat_long_bounds(self):
        '''
            Override the lat long boundaries with [1,1,2,2]. Given these boundaries, only one node should be added
        '''
        self.queue = MapTraversalQueue([1,1,2,2],self.mock_api,self.mock_cache)
        node_coordinates = reduce(lambda x,y: x + [y.coordinates()],self.queue.nodes,[])
        node_coordinates.sort()
        self.assertEquals(node_coordinates,[[1.0, 1.0, 2.0, 2.0]])

    def test_process_nodes(self):
        '''
            verify that the process_nodes function looks to grab unprocessed nodes and called their process method
            previously processed nodes should not be reprocessed
            Objective:
                - override the nodes with mocked up nodes
                - set one of them to unprocessed
                - trigger the queue process_nodes method, verify one node gets processed and the remaining do not
        '''

        self.queue.nodes = []
        for i in range(0,4):
            node = mock.create_autospec(MapTraversalNode)
            node.processed = True
            self.queue.nodes.append(node)

        self.queue.nodes[2].processed = False
        self.queue.process_nodes()
        self.queue.nodes[2].process.assert_called_with()
        self.queue.nodes[3].process.assert_not_called()


if __name__ == '__main__':
    unittest.main()
