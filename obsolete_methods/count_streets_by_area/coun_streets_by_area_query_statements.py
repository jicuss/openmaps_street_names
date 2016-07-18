def country_query(name='United States of America'):
        query = u"""
    area[admin_level=2]["name"='{}'][boundary=administrative][border_type=national]->.countryboundaryarea;
    (node[place="state"](area.countryboundaryarea););
    out;
    """.format(name)

        return query

def state_query(name='California'):
        '''
        This query is currently restricted to US states only by the addition of the ['ISO3166-2'~"^US-"] clause.
        In the event you want to modify this script for international support, youll need to rework this.
        '''
        query = u"""
    area[admin_level=4]["name"="{}"][boundary=administrative]['ISO3166-2'~"^US-"]->.stateboundaryarea;
    (node[place="city"](area.stateboundaryarea););out;
    out;
    """.format(name)

        return query

def city_query(city_name='Escondido',state_name='California'):
        # removed [border_type=city] as it caused issues for some cities
        query = u"""
    area[admin_level=8][name="{}"][boundary=administrative]['is_in:state'='{}']->.boundaryarea;
    way(area.boundaryarea)[highway~"^(tertiary|residential)$"];
    (._;>;);
    out body;
    """.format(city_name,state_name)

        return query

def city_query_alternative(city_name='Escondido',state_name='California'):
        ''' due to incomplete metadata in the openmaps API, some cities require a different approach
        For instance, La Habra Heights in California is not associated with the state, as a result the previous query returns no results
         '''
        query = u"""
    area[admin_level=8][name="{}"][boundary=administrative][place~"^(city|town)$"]->.boundaryarea;
    way(area.boundaryarea)[highway~"^(tertiary|residential)$"];
    (._;>;);
    out body;
    """.format(city_name)

        return query

def city_query_alternative_b(city_name='Escondido',state_name='California'):
        ''' due to incomplete metadata in the openmaps API, some cities require a different approach
        For instance, La Habra Heights in California is not associated with the state, as a result the previous query returns no results
         '''
        query = u"""
    area[admin_level=8][name="{}"][boundary=administrative][border_type=city]->.boundaryarea;
    way(area.boundaryarea)[highway~"^(tertiary|residential)$"];
    (._;>;);
    out body;
    """.format(city_name)

        return query




