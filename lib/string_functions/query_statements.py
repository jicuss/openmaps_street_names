'''
                                           OVERPASS API QUERY GENERATORS
'''

def box_query_residential(coordinates):
    '''
        This function is used generate an Overpass API query. This is the main function used to collect street name data
        It:
            - specifies a lat long coordinate box to request ways data from
            - explicitly declares a timeout of 180s. In testing this parameter was not reliable
            - selects all residential or main artery ways.
    '''
    south, west, north, east = coordinates
    query = u"""
        [timeout:180]
        [bbox:{},{},{},{}];
        way[highway~"^(tertiary|living_street|residential)$"];
        out body; """.format(south, west, north, east)

    return query


def box_query_all(coordinates):
    '''
        This function is used generate an Overpass API query
        It:
            - specifies a lat long coordinate box to request ways data from
            - explicitly declares a timeout of 180s. In testing this parameter was not reliable
            - selects all ways available
    '''
    south, west, north, east = coordinates
    query = u"""
        [bbox:{},{},{},{}];
        way[highway];
        out body; """.format(south, west, north, east)

    return query
