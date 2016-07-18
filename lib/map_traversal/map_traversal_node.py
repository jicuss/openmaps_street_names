import logging

from lib.overpass.overpass_api_cache import OverpassAPICache
from lib.string_functions.string_operations import fragment_key_formatting

from lib.overpass.overpass_api import OverpassAPI
from lib.string_functions.query_statements import box_query_residential

logger = logging.getLogger('')

class MapTraversalNode():
    def __init__(self, coordinates, api = OverpassAPI(), cache = OverpassAPICache()):
        self.processed = False
        self.south, self.west, self.north, self.east = coordinates
        self.api = api
        self.cache = cache
        self.response = {'ways': []}

        '''
            round the coordinates
            the node expects integer lat long coordinates.
        '''
        self.south = round(self.south, 0)
        self.west = round(self.west, 0)
        self.north = round(self.north, 0)
        self.east = round(self.east, 0)

    def coordinates(self):
        '''
            Returns an array of the coordinates in the format [south,west,north,east]

            From the docs:
            - left is the longitude of the left (westernmost) side of the bounding box.
            - bottom is the latitude of the bottom (southernmost) side of the bounding box.
            - right is the longitude of the right (easternmost) side of the bounding box.
            - top is the latitude of the top (northernmost) side of the bounding box.
        '''
        return [self.south, self.west, self.north, self.east]

    def fragment_key(self):
        '''
            Returns a string composed of the coordinates
            This is used to store and retrieve the node data from the cache
        '''
        key = '_'.join(['coordinate', str(self.south), str(self.west), str(self.north), str(self.east)])
        return fragment_key_formatting(key)

    def process(self):
        '''
            This method is called by the queue. It looks to see if the fragment_key for the coordinates exists in the cache
             - If it exists, returns the fragment
             - If not exists, calls the API
        '''
        if not self.processed:
            logger.info("Processing Node {}".format(self.fragment_key()))
            # todo, remove this where clause, prevents preproccesed nodes from being handled
            '''
            if not self.cache.cache_fragment_exists(self.fragment_key()):
                # todo, remove this try catch
                try:
                    self.response = self.api.query_api(box_query_residential(self.coordinates()), self.fragment_key())
                except:
                    self.processed = True
            '''
            self.response = self.api.query_api(box_query_residential(self.coordinates()), self.fragment_key())
            self.processed = True