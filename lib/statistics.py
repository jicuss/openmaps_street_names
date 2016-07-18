import logging
import redis
from lib.map_traversal.map_traversal_queue import MapTraversalQueue
from lib.string_functions.string_operations import state_postal_codes, strip_state_postal_codes, remove_blacklisted_words

logger = logging.getLogger('')

class StreetNameStatistics():
    def __init__(self, queue):
        self.queue = queue

        if not isinstance(queue, MapTraversalQueue):
            raise TypeError,'The Queue needs to be of MapTraversalQueue type'

        self.establish_redis_cache()

    def establish_redis_cache(self):
        logger.info("Establishing Redis Cache")
        self.redisObj = redis.StrictRedis(host='localhost', port=6379, db=0)

    def wipe_redis(self):
        logger.info("Wiping Redis Cache")
        keys = ['street_ids', 'county_count', 'streets', 'streets_normalized', 'street_*', 'word_count']
        for key in keys:
            self.redisObj.delete(key)

    def process_node(self, node):
        node.process()

        if 'ways' in node.response:
            for street in node.response['ways']:

                ''' if the tiger:county key is not defined in the way tags, skip the road and do not process it. '''
                if 'tiger:county' not in street['tags']:
                    continue

                '''
                    Check to see if the state postal codes in the tiger:county key are in the continental US
                    This excludes roads that are possibly in Canada or Mexico and prevents the rare user defined non existent road from being counted
                    The strip_state_postal_codes function parses the postal codes out of the tiger:county code
                    The state_postal_codes function contains a list of valid US government postal codes
                '''
                valid_postal_codes = state_postal_codes()
                street_postal_codes_in_us = map(lambda x: x in valid_postal_codes, strip_state_postal_codes(street['tags']['tiger:county']))

                if True not in street_postal_codes_in_us:
                    continue

                '''
                   if the name key is available, use that as the street name, with the next best option being name:en. Otherwise default to 'n/a'
                '''
                street_name = 'n/a'

                if 'name' in street['tags']:
                    street_name = street['tags']['name']

                elif 'name:en' in street['tags']:
                    street_name = street['tags']['name:en']

                '''
                    Count the occurrences of the unnormalized street names
                    This operation increments a key corresponding to the street name in a Redis hash.
                    I used Redis as it seems to handle memory much more efficiently than the standard python hash implementation
                '''

                logger.debug(u"Adding Street - {}".format(street_name))
                self.redisObj.hincrby('streets', street_name, 1)
                logger.debug(u"Street {} - {}".format(street_name, self.redisObj.hget('streets', street_name)))

                '''
                    Count the occurrences of the normalized street name
                    There were many common prefixes and suffixes that prevented nearly identical street names from being counted as the same street.
                    It would be interesting to see the relative prevalence of street names if only the main root street name was used.
                    For example North Main Street, Main Street, and Main Avenue would all be treated as a single street named Main
                    What would the most common root street names be?
                '''
                blacklisted_words = ["Road", "Street", "Drive", "Avenue", "Lane", "Court", "North", "East", "West",
                                     "South", "Circle", "Place", "Way", "Northeast", "Northwest", "Southeast",
                                     "Southwest", "Boulevard"]

                normalized_street_name = remove_blacklisted_words(street_name, blacklisted_words)
                self.redisObj.hincrby('streets_normalized', normalized_street_name, 1)

                '''
                    count the occurrences of a specific words in the street name
                '''
                for word in street_name.split(' '):
                    self.redisObj.hincrby('word_count', word, 1)

        node.response = {}  # clear the node response to free up memory

    def count_streets(self):
        self.wipe_redis()
        logger.info("Counting the Occurrences of Street Names")

        for node in self.queue.nodes:
            '''
                rather than process all nodes at once, process each node individually then eliminate its response to free up memory
            '''
            self.process_node(node)

        ''' unnormalized street name count '''
        logger.debug(u"Steet Name Count")
        self.redisObj.hdel('streets', 'n/a')  # remove the count of streets with no defined name
        self.print_and_store_results('streets', 'street_name_occurances.txt')

        ''' normalized street name count '''
        logger.debug(u"Normalized Steet Name Count")
        self.redisObj.hdel('streets_normalized', 'n/a', '')  # remove the count of streets with no defined name
        self.print_and_store_results('streets_normalized', 'normalized_street_name_occurances.txt')

        ''' word count '''
        logger.debug(u"Word Count")
        self.print_and_store_results('word_count', 'word_occurrences.txt')

    def fetch_results(self, redis_key, output_file = None):
        '''
            Looks into a Redis hash within the key redis_key
            Convert the value for each key in the hash from a string to an int (redis returns strings by default)
            Stores the results in a tab delimited file specified by output_file
        '''

        count_hash = self.redisObj.hgetall(redis_key)
        for key in count_hash.keys():
            count_hash[key] = int(count_hash[key])

        sorted_keys = sorted(count_hash, key=count_hash.get, reverse=True)

        if output_file:
            with open(output_file, 'w') as f:
                for k in sorted_keys:
                    f.writelines('\t'.join([str(k), str(count_hash[k]), '\n']))

        return {'sorted_keys': sorted_keys, 'count_hash': count_hash}

    def print_and_store_results(self, redis_key, output_file):
        '''
            Prints the top 10 most common results (if 10 available)
        '''
        results = self.fetch_results(redis_key, output_file)
        count_hash = results['count_hash']
        sorted_keys = results['sorted_keys']

        max_range = len(sorted_keys)
        if max_range > 10:
            max_range = 10

        for k in range(0, max_range):
            print sorted_keys[k], count_hash[sorted_keys[k]]

