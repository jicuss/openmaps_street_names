'''
                                               OVERPASS API WRAPPER

    This is a wrapper for the Overpy library. All queries will be issued through an instance of this class.
    Operations:
        - Check to see if an API request has been issued before
        - If request has been issued before, return the results of the previous query
        - If request has not been issued before, issue request and store the results in the cache.

    This response caching strategy will lesson the burden on the Overpass API by eliminating duplicate API calls as we collect street data
'''

import logging
import sys
from time import sleep

import overpy

from lib.external_resources.timeout import timeout
from lib.overpass.overpass_api_cache import OverpassAPICache

logger = logging.getLogger('')


class OverpassAPI():
    def __init__(self, overpy_instance=overpy.Overpass(), cache=OverpassAPICache()):
        self.overpy_instance = overpy_instance
        self.cache = cache

    def query_api(self, query, fragment_key):
        '''
            :param query: An Overpass API query that will be issued using an instance of an Overpy object
            :param fragment_key: A unique query identifier used to store and retrieve the results of an API query.
            :return: a hash object in the structure of {'nodes':array(nodes),'ways': array(ways)}
        '''

        if self.cache.cache_fragment_exists(fragment_key):
            logger.info(u"Requesting Cache Fragment: {}".format(fragment_key))
            return self.cache.load_cache_fragment(fragment_key)

        else:
            '''
                Issue the API request.
                Operations:
                    - Issue and API request to the Openmaps API using the Overpy library. Delay next request by 15 seconds
                    - In the event of a OverpassTooManyRequests exception, sleep for 120 seconds
                    - In the event of an unexpected error sleep for 15 seconds.

                Notes:
                    - During the day the Overpass API is more apt to return with a OverpassTooManyRequests error.
                    - Adding the a sleep after failed requests, and running the scripts overnight greatly improved the rate of API call success
            '''
            logger.info(u"Making API Service Call\n{}".format(query))
            while True:
                '''
                    Try to make the API request. In the event of a failure, retry indefinitely. If successful, break from the loop
                '''
                try:
                    '''
                        There is an 180s timeout on all API calls. This is in addition to the 180s timeout parameter specified in the Overmaps API request
                        Originally I felt the timeout specified in the API query would be sufficient. In testing it was found that in some cases the server
                        did not properly return and the overpy class instance would sit idle indefinitely.
                    '''
                    with timeout(seconds=180):
                        api_response = self.overpy_instance.query(query.encode('utf8'))

                    sleep(30)  # added a sleep function to lesson the burden on the openmaps api. Not explicitly required

                except overpy.exception.OverpassTooManyRequests:
                    logger.info("OverpassTooManyRequests. This occurs when the script is spamming the OverpassAPI service. Sleeping for 120s".format(query))
                    sleep(120)
                    continue

                except:
                    logger.info("Unexpected error:".format(sys.exc_info()))
                    sleep(15)
                    continue

                break

            '''
                Convert the overpy object to a cache friendly format, return the response.
                Operations:
                    - For each of the nodes and ways, convert the overpy data type to a hash.
                    - Remove unused keys. This may be unnecessary given the limited size of the dataset.
                    - Store final hash response in the cache
            '''

            '''
                convert Overpass Result object to a hash, keep only the relevant keys
            '''
            blacklisted_keys = ['_result', '_node_ids', 'lon', 'lat']

            nodes = []
            for node in api_response.nodes:
                hash = node.__dict__
                for key in blacklisted_keys:
                    if key in hash:
                        del hash[key]

                nodes.append(hash)

            ways = []
            for way in api_response.ways:
                hash = way.__dict__
                for key in blacklisted_keys:
                    if key in hash:
                        del hash[key]

                ways.append(hash)

            '''
                Store the final response in the cache then return the response
            '''
            final_response = {'nodes': nodes, 'ways': ways}
            self.cache.store_cache_fragment(fragment_key, final_response)

            return final_response
