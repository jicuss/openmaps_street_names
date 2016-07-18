import datetime
import logging
import os
import pdb

import overpy
from lib.overpass.overpass_api_cache import OverpassAPICache
from lib.map_traversal.map_traversal_queue import MapTraversalQueue
from lib.overpass.overpass_api import OverpassAPI
from lib.statistics import StreetNameStatistics

logger = logging.getLogger('')

def main(logLevel, logFile):
    logFormat = '%(asctime)s : filename=%(filename)s : threadname=%(threadName)s : linenumber=%(lineno)d : messageType=%(levelname)s : %(message)s'

    logging.basicConfig(filename=logFile, filemode='a+', level=logLevel, format=logFormat)

    console = logging.StreamHandler()  # forces logging to the console so user can track progress
    console.setLevel(logging.DEBUG)

    logging.getLogger('').addHandler(console)  # add the handler to the root logger

    cache = OverpassAPICache('cache_complete_us')
    api = OverpassAPI(overpy.Overpass(), cache)

    '''
        Second Approach. Navigate using lat longs
        Examples:
            MapTraversalQueue([32.5, -118.6, 34.1, -114.7]) # san diego
            MapTraversalQueue([42.1, -83.4, 43.17, -81.43]) # michigan
            MapTraversalQueue([25.87,-124.45,48.75,-64.68]) # complete US, small bit of mexico and Canada
    '''
    queue = MapTraversalQueue([25.87,-124.45,48.75,-64.68], api, cache)
    stats = StreetNameStatistics(queue)
    stats.count_streets()


if __name__ == "__main__":
    log_path = os.path.abspath(os.path.join(__file__, '..', 'logs/'))
    main(logging.DEBUG, log_path + '/' + str(datetime.datetime.now().isoformat()) + "-street_name_count.log")
