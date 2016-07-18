import unittest
import overpy
import mock
import pdb
import random

from lib.string_functions.string_operations import fragment_key_formatting
from lib.statistics import StreetNameStatistics
from lib.overpass.overpass_api_cache import OverpassAPICache
from lib.map_traversal.map_traversal_queue import MapTraversalQueue
from lib.overpass.overpass_api import OverpassAPI


class OverpassAPICacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''
            This method is run only once at the beginning of the test.
            It:
                - Generates a fake dataset
                - Collects stats about the occurences of the street names in the fake dataset
                - Makes the results of that analysis available to all tests

            This is more of an integrated functionality test than a unit test as it does rely on the supporting libraries to function
        '''
        OverpassAPICacheTests.generate_fake_dataset()

        super(OverpassAPICacheTests, cls).setUpClass()
        cls.cache = OverpassAPICache('cache_fake')
        cls.api = OverpassAPI(overpy.Overpass(), cls.cache)
        cls.queue = MapTraversalQueue([32.5, -118.6, 34.1, -114.7], cls.api, cls.cache)
        cls.stats = StreetNameStatistics(cls.queue)
        cls.stats.count_streets()

    @classmethod
    def generate_fake_dataset(cls):
        ''' the point of this method is to generate a fake dataset so I can test my counting routines '''
        api = mock.create_autospec(overpy.Overpass)
        cache = OverpassAPICache('cache_fake')
        queue = MapTraversalQueue([32.5, -118.6, 34.1, -114.7], api, cache)

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
            for i in range(0, name_occurance[key]):
                data_queue.append({"tags": {"name": key, "tiger:county": "San Diego, CA"}})

        ''' randomize the order of the fake data, not neccesary but better emulates the response of openmaps '''
        random.shuffle(data_queue)

        ''' add the way to a random node '''
        while len(data_queue) > 0:
            node = queue.nodes[random.randint(0, len(queue.nodes) - 1)]
            node.response['ways'].append(data_queue.pop())

        for node in queue.nodes:
            fragment_key = fragment_key_formatting(node.fragment_key())
            queue.cache.store_cache_fragment(fragment_key, node.response)

    def setUp(self):
        pass

    def test_exclusion_of_invalid_county(self):
        ''' verifies that streets without a valid county are not being included in the result set '''
        pass

    def test_exclusion_of_invalid_postal_code(self):
        ''' verifies that streets without a valid postal code are not being included in the result set '''
        pass

    def test_unnormalized_street_name_count(self):
        ''' verifies that streets names are being properly counted '''

        pass

    def test_normalized_street_name_count(self):
        '''
            Verify that street names are being properly grouped after normalization.  Verifies both the name normalization routine and the counting is correct
        '''
        pass

    def test_blacklisted_words_removal(self):
        '''
            Verify that words contained in the blacklist are being properly removed prior to being counted in the normalized street name count
        '''
        pass

    def test_word_count(self):
        ''' verifies that word occurances are being properly counted '''

        pass


if __name__ == '__main__':
    unittest.main()
