import logging

from lib.overpass.overpass_api_cache import OverpassAPICache

from lib.map_traversal.map_traversal_node import MapTraversalNode
from lib.overpass.overpass_api import OverpassAPI

logger = logging.getLogger('')

class MapTraversalQueue():
    def __init__(self, boundaries, api = OverpassAPI(), cache = OverpassAPICache()):
        self.queue = []
        self.nodes = []
        self.api = api
        self.cache = cache
        self.lat_long_box_length = 1
        self.south_bound, self.west_bound, self.north_bound, self.east_bound = boundaries
        self.add_initial_node()
        self.traverse_bounds()
        # self.process_nodes()

    def add_initial_node(self):
        '''
            add a starting point to the queue. I chose to iterate from southwest to northeast. The starting point is the farthest southwest corner
        '''
        logger.info(u"Adding Initial Node")
        starting_coordinates = [self.south_bound, self.west_bound, self.south_bound + self.lat_long_box_length, self.west_bound + self.lat_long_box_length]
        self.queue.append(MapTraversalNode(starting_coordinates, self.api, self.cache))

    def traverse_bounds(self):
        '''
            adds a node for each lat long box in the geographical US.
        '''
        while len(self.queue) > 0:
            node = self.queue.pop()
            self.nodes.append(node)

            if (node.north + self.lat_long_box_length) <= self.north_bound:
                ''' move south to north if traversed to north boundary '''
                logger.info("Appending New Node, Incremented to the North")
                self.queue.append( MapTraversalNode([node.north, node.west, node.north + self.lat_long_box_length, node.east], self.api, self.cache))

            elif (node.east + self.lat_long_box_length) <= self.east_bound:
                ''' move west to east. if traversed to east boundary do nothing'''
                logger.info("Appending New Node, Incremented to the East")
                self.queue.append(MapTraversalNode( [self.south_bound, node.east, self.south_bound + self.lat_long_box_length, node.east + self.lat_long_box_length], self.api, self.cache))

    def process_nodes(self):
        '''
            iterate through each of the nodes and download their map data
        '''

        for node in filter(lambda x: x.processed != True, self.nodes):
            node.process()
