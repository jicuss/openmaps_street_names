import datetime
import logging
import os
import random

import mock
import overpy

from lib.map_traversal.map_traversal_queue import MapTraversalQueue
from lib.overpass.overpass_api_cache import OverpassAPICache
from lib.string_functions.string_operations import fragment_key_formatting

logger = logging.getLogger('')

def main(logLevel, logFile):
    logFormat = '%(asctime)s : filename=%(filename)s : threadname=%(threadName)s : linenumber=%(lineno)d : messageType=%(levelname)s : %(message)s'

    logging.basicConfig(filename=logFile, filemode='a+', level=logLevel, format=logFormat)

    '''
    Forces logging to the console so user can track progress
    '''
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    api = mock.create_autospec(overpy.Overpass)
    cache = OverpassAPICache('cache_fake')

    ''' the point of this script is to generate a fake dataset so I can test my counting routines '''

    logging.info('Generating Fake Dataset for Testing')
    queue = MapTraversalQueue([32.5, -118.6, 34.1, -114.7],api,cache)

    name_occurance = {'Main Street': 23,
                      '215th Avenue': 5,
                      'Jefferson Street': 8,
                      'Ohio': 25,
                      '220th': 1,
                      'North Main Street': 15,
                      'Walnut Street': 16,
                      'County Road': 11,
                      '180th': 6,
                      'Terre Haute Road': 5,
                      '125th Avenue': 1
                      }

    data_queue = []
    for key in name_occurance.keys():
        for i in range(0,name_occurance[key]):
            data_queue.append({ "tags": { "name": key, "tiger:county": "San Diego, CA" } })

    ''' randomize the order of the fake data, not neccesary but better emulates the response of openmaps '''
    random.shuffle(data_queue)

    ''' add the way to a random node '''
    while len(data_queue) > 0:
        node = queue.nodes[random.randint(0,len(queue.nodes)-1)]
        node.data['ways'].append(data_queue.pop())

    for node in queue.nodes:
        fragment_key = fragment_key_formatting(node.coordinate_fragment_key())
        queue.cache.store_cache_fragment(fragment_key, node.data)

if __name__ == "__main__":
    log_path = os.path.abspath(os.path.join(__file__, '..', 'logs/'))
    main(logging.DEBUG, log_path + '/' + str(datetime.datetime.now().isoformat()) + "-street_name_count.log")
