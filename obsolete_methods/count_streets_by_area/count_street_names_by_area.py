'''
                                          Failed Attempt: Find Streets By Area
This script was my first attempt at counting all streets in the US. In the end I realized this was a flawed approach.
Clearly I could not request all streets in the US with one API call. I needed to break the API calls into discrete units
small enough that the Openmaps server could respond in a limited amount of time. My plan was to grab all states in the US,
iterate through the states to grab all cities, then grab the streets in each of the cities. What I found was that the
metadata for cities was pretty inconsistent. This meant that the API query used to return the ways for a given city
did not consistently return valid results. Lets look at a few examples of how this approach failed to return valid queries.

Best Case:
Escondido, CA
https://www.openstreetmap.org/relation/253832
admin_level - 8
border_type - city
boundary - administrative
is_in:state - California
name - Escondido
place - city


Notice that the is_in:state metadata key associates the city correctly with the state. This meant that if I searched for Escondido,
I could scope the results to only streets Escondido, CA. If another Escondido existed in the world, results for that town would not be returned.

Escondido, CA is next to San Diego, CA. Results for San Diego were not being returned correctly. Lets look at the metadata stored for San Diego.

San Diego, CA
https://www.openstreetmap.org/relation/253832
admin_level - 8
border_type - city
boundary - administrative
name - San Diego
place - city

In this case, the is_in:state key is not defined. This prevented the previous query that included the is_in:state key from operating properly.
I ended up writing an alternative query that would get called in the event that no ways being returned and continued with the project.

This approach again hit a snag when I realized that Denver, CO was returning results for Denver, CO

Berkley, CA
https://www.openstreetmap.org/relation/2833528
admin_level - 8
boundary - administrative
is_in:state_code - CA

In this case, the place key is undefined, as is the border type. This once again prevented the API queries from operating properly.
Rather than try and make queries for every edge case required to return valid responses for all cities, I started a new approach
where I applied lat long boundaries then iterated traversed the US. This didn’t rely on the city metadata to be correct, but did
by default include small portions of Mexico and Canada that would need to be excluded during the final street count tally.
'''

import datetime
import logging
import os
import pdb

from lib.overpass_api_cache import OverpassAPICache

from lib.overpass.overpass_api import OverpassAPI
from lib.string_functions.string_operations import fragment_key_formatting
from obsolete_methods.count_streets_by_area import city_query,state_query,country_query

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

    api = OverpassAPI()
    cache = OverpassAPICache()

    '''
    First, lets grab all states in the US.
    By default, OpenMaps will return Virgin Islands & Puerto Rico in the list of US states.
    Remember to exclude those from our list of states
    '''
    fragment_key = fragment_key_formatting('country_usa')
    response = api.query_api(country_query('United States of America'),fragment_key)

    '''
    First, lets grab all states in the US.
    By default, OpenMaps will return Virgin Islands & Puerto Rico in the list of US states.
    Remember to exclude those from our list of states
    '''
    states = []
    for state in response['nodes']:

        ''' try to assign a shortname to the state. PR and VR do not have valid shortnames '''
        abv = ''
        if 'name:short' in state['tags']:
            abv = state['tags']['name:short']
        elif 'ref' in state['tags']:
            abv = state['tags']['ref']

        if abv != '':
            states.append({'name': state['tags']['name'], 'shortname': abv})

    ''' now remove Virgin Islands & Puerto Rico from the list of states'''
    states = filter(lambda x: x not in ['United States Virgin Islands','Puerto Rico'],states)

    '''
    For each state, grab a list of cities in the state
    '''
    cities = []
    for state in states:
        fragment_key = fragment_key_formatting('state_{}'.format(state['name']))
        response = api.query_api(state_query(state['name']),fragment_key)
        if 'nodes' in response:
            for city in response['nodes']:
                ''' most cities have a name tag, for some areas (specifically Hawaii) the name:en is used '''

                if 'name' in city['tags']:
                    cities.append({'state': state['name'], 'state_shortname': state['shortname'],'city': city['tags']['name']})
                elif 'name:en' in city['tags']:
                    cities.append({'state': state['name'],'state_shortname': state['shortname'], 'city': city['tags']['name:en']})

    '''
    For each city, grab a list of strees in the city. Be aware that duplicate instances of street objects are common.
    For now we are going to generate a word count, to complete the assignment we need to generate a street name count
    '''
    word_count = {}
    street_name_count = {}
    rejects = []
    for city in cities:
        # todo: Looks like some cities with unicode characters in their are occasionally not returning street results from openmaps.
        # todo: Also, the same street is considered a unique street when it crosses city boundaries

        fragment_key = fragment_key_formatting(u'city_{}_{}'.format(city['state'],city['city']))
        response = api.query_api(city_query(city['city'],city['state']),fragment_key)

        ''' inspect the county, verify that its in the correct state. Remove form cache if in wrong state '''

        if 'ways' in response:
            for way in response['ways']:
                if 'tiger:county' in way['tags']:
                    try:
                        first_city = way['tags']['tiger:county'].split(';')[0]
                        first_city = first_city.split(':')[0]
                        county,state_abv = first_city.split(', ')
                    except:
                        ''
                    if state_abv != city['state_shortname']:
                        rejects.append(fragment_key)
        '''
        in testing it was found that some cities were not returning any street results.
        The metadata explorer available @ https://www.openstreetmap.org/relation/3529698
        show that these cities were not correctly associated with their state. In cases where not results are returned,
        attempt to use city_query_alternative
         '''
        if 'ways' in response and len(response['ways']) == 0:
            cache.clear_cache_fragment(fragment_key)
            #response = api.query_api(city_query_alternative(city['city'],city['state']),fragment_key)
            #response = api.query_api(city_query_alternative_b(city['city'],city['state']),fragment_key)


        city_streets = [] # contains a uniq list of streets already processed for this city object
        if 'ways' in response:
            for street in response['ways']:
                street_name = 'n/a'
                if 'name' in street['tags']:
                    street_name = street['tags']['name']
                elif 'name:en' in street['tags']:
                    street_name = street['tags']['name:en']

                if street_name not in city_streets:
                    city_streets.append(street_name) # prevents duplicate street instances in the same street from being counted twice

                    ''' word count logic '''
                    words = ' '.split(street_name)

                    for word in words:
                        if word in word_count:
                            word_count[word] += 1
                        else:
                            word_count[word] = 1

                    ''' street name count logic. Need to verify the steets are in fact unique '''
                    if street_name in street_name_count:
                        street_name_count[street_name] += 1
                    else:
                        street_name_count[street_name] = 1

    ''' print the most common streets '''
    del(street_name_count['n/a']) # remove streets with no defined name
    sorted_keys = sorted(street_name_count, key=street_name_count.get, reverse=True)
    for k in range(0,10):
        print sorted_keys[k], street_name_count[sorted_keys[k]]


    rejects = list(set(rejects))

    pdb.set_trace()

if __name__ == "__main__":
    log_path = os.path.abspath(os.path.join(__file__,'..', '..', 'logs/'))
    main(logging.DEBUG, log_path + '/' + str(datetime.datetime.now().isoformat()) + "-street_name_count.log")
