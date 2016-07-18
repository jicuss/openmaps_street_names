import unittest
import overpy
import mock
import pdb
import random
import os

from lib.string_functions.string_operations import fragment_key_formatting
from lib.statistics import StreetNameStatistics
from lib.overpass.overpass_api_cache import OverpassAPICache
from lib.map_traversal.map_traversal_queue import MapTraversalQueue
from lib.overpass.overpass_api import OverpassAPI


class OverpassAPICacheTests(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        for f in ["word_occurrences.txt", "street_name_occurances.txt", "normalized_street_name_occurances.txt"]:
            os.remove(f)

    @classmethod
    def setUpClass(cls):
        '''
            This method is run only once at the beginning of the test.
            It:
                - Generates a fake dataset
                - Collects stats about the occurrences of the street names in the fake dataset
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

        cls.name_occurrence = {'125th Avenue': 1, '220th': 1, '215th Avenue': 5, 'Jefferson Street': 8, '180th': 6, 'Ohio': 25, 'North Main Street': 15, 'Walnut Street': 16, 'County Road': 11, 'Terre Haute Road': 5, 'Main Street': 23}
        cls.normalized_name_occurrence = {'180th': 6, '220th': 1, 'Terre Haute': 5, 'Walnut': 16, 'County': 11, '215th': 5, 'Jefferson': 8, '125th': 1, 'Ohio': 25, 'Main': 38}
        cls.word_occurrence = {'North': 15, 'Haute': 5, 'Terre': 5, '180th': 6, '220th': 1, 'Walnut': 16, 'County': 11, '215th': 5, 'Jefferson': 8, '125th': 1, 'Ohio': 25, 'Main': 38, 'Avenue': 6, 'Road': 16, 'Street': 62}

        data_queue = []
        for key in cls.name_occurrence.keys():
            for i in range(0, cls.name_occurrence[key]):
                data_queue.append({"tags": {"name": key, "tiger:county": "San Diego, CA"}})

        ''' add invalid tiger:county record '''
        data_queue.append({"tags": {"name": 'InvalidCountyRecord'}})

        ''' add invalid postal code record '''
        data_queue.append({"tags": {"name": 'InvalidPostalCodeRecord', "tiger:county": "Bogustown, NT"}})

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
        self.assertNotIn('InvalidCountyRecord',self.stats.fetch_results('streets')['sorted_keys'])

    def test_exclusion_of_invalid_postal_code(self):
        ''' verifies that streets without a valid postal code are not being included in the result set '''
        self.assertNotIn('InvalidPostalCodeRecord',self.stats.fetch_results('streets')['sorted_keys'])

    def test_unnormalized_street_name_count(self):
        ''' verifies that streets names are being properly counted '''
        for street in self.name_occurrence:
            self.assertEquals(self.stats.fetch_results('streets')['count_hash'][street],self.name_occurrence[street])

    def test_normalized_street_name_count(self):
        '''
            Verify that street names are being properly grouped after normalization.
            Verifies both the name normalization routine and the counting is correct
        '''
        for street in self.normalized_name_occurrence:
            self.assertEquals(self.stats.fetch_results('streets_normalized')['count_hash'][street],self.normalized_name_occurrence[street])

    def test_word_count(self):
        ''' verifies that word occurrences are being properly counted '''
        for word in self.word_occurrence:
            self.assertEquals(self.stats.fetch_results('word_count')['count_hash'][word],self.word_occurrence[word])

if __name__ == '__main__':
    unittest.main()
