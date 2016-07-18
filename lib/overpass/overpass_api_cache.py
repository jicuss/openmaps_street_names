'''
                                                OVERPASS API CACHE
    This class caches arbitrary data. We will be using it to store the response of the Overpass API to eliminate duplicate API calls
    Operations:
        - In the context of the cache the piece of data being stored is refered to as the 'fragment'
        - The string used to identify the fragment of information stored is refereed to as the 'fragment_key'
        - The cache stored the fragment in a file named as the fragment_key.
            - Currently this is done on disk.
            - Using an in memory cache such as Redis would greatly improve the speed that the fragment could be returned.
        - For this class fragments are dictionary objects. When stored on disk they are rendered as JSON objects and written to the file
        - When retrieving the fragment, the JSON file is converted back to a dictionary and returned

'''
import logging
import os
import json
import shutil
import pdb

logger = logging.getLogger('')

class OverpassAPICache():
    def __init__(self, relative_cache_path='cache'):
        self.cache_path = os.path.abspath(os.path.join(__file__,'..','..','..', relative_cache_path))
        self.establish_directory_structure()

    def establish_directory_structure(self):
        '''
            Recursively establish a directory to hold the cache data.
        '''
        if not os.path.exists(self.cache_path):
            logger.debug("Establishing Cache: {}".format(self.cache_path))
            os.makedirs(self.cache_path)

    def fragment_cache_path(self, fragment_key):
        '''
            Generate an absolute path for the cache fragment
        '''
        return os.path.join(self.cache_path, fragment_key)

    def cache_fragment_exists(self, fragment_key):
        '''
            Test if the cache fragment exists in the cache directory
        '''
        if os.path.exists(self.fragment_cache_path(fragment_key)):
            return True

    def load_cache_fragment(self, fragment_key):
        '''
            If the cache fragment exists in the cache directory, load the fragment.
            This function assumes the fragment was stored in JSON format.
        '''

        logger.debug(u"Fetching Cache Fragment: {}".format(fragment_key))
        fragment_content = []
        if self.cache_fragment_exists(fragment_key):
            with open(self.fragment_cache_path(fragment_key), 'r') as f:
                for line in f:
                    fragment_content.append(line)

            return json.loads(''.join(fragment_content))
        else:
            logger.debug(u"Cache Fragment {} Unavailable".format(fragment_key))

    def store_cache_fragment(self, fragment_key, data):
        '''
            Given a dictionary data object, store it in the cache directory in a json formatted file with the file name specified by the fragment_key
        '''
        logger.debug(u"Storing Cache Fragment: {}".format(fragment_key))
        with open(self.fragment_cache_path(fragment_key), 'w') as f:
            f.writelines(json.dumps(data))

    def clear_cache_fragment(self, fragment_key):
        '''
            If the cache fragment exists, delete the fragment from the cache folder
        '''
        logger.debug(u"Clearing Cache Fragment: {}".format(fragment_key))
        if self.cache_fragment_exists(fragment_key):
            os.remove(self.fragment_cache_path(fragment_key))
            return True
