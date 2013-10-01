# coding: utf-8


####################### To Do list ##################################
#TODO remove all methods which involve writing , or the feature part. after pickling the data.


__author__ = 'kobi_luria'

import requests
import json
import objects
import os
import tools
import pickle

################## END_POINTS  #################################:

NOMINATIM = 'http://nominatim.openstreetmap.org/search?accept-language=en-us&q='
NOMINATIM_FORMAT = '&format=json&polygon_geojson=1&addressdetails=1'
API = 'http://api.dev.openmuni.org.il/'
VERSION = 'v1/'
ENTITIES = 'entities/'
DIR_PROJECT = '/home/kobi/projects/open_gis'
DIR = '/home/kobi/projects/open_gis/maps'
GEO_JSON = '.geojson'

#################################################################


def write_to_file(parent_path, name_en, json_object):
    """
    write a polygon object which is a muni or district to file. this method will produce all
    the folders and file for the single muni and district files.

    :param parent_path: the parent path to write this file
    :param name_en: the name of the file or object.
    :param json_object: the json object which is written to file.
    :return:
    """
    dir_path = os.path.join(DIR, parent_path).rstrip(name_en).replace(' ', '_').lower()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    path = os.path.join(dir_path, name_en + GEO_JSON).replace(' ', '_').lower()
    f = open(path, 'w+')
    json.dump(json_object, f)


def make_feature(json_polygon, json_properties):
    """
    make a feature geojson from a json-polygon object.
    this function just wrappes the polygon and the feature properties
    into the the json feature. the properties can then be viewed in any map!
    :param json_polygon: the polygon of a muni or district.
    :param json_properties: the properties which are added on to the coordinate polygon.
    :return: the feature which is a coordinates and properties.
    """
    feature = {'type': 'Feature', 'geometry': json_polygon, 'properties': json_properties}
    return feature


def get_geojson_for_muni(search_string):
    """
    this funcction gets the geo GIS coordinate for each entity.
    the function currently calles the NOMINATIM server with a search string.
    The only case which a result is picked is if the osm-type is a relation i.e its
    a entity in the open street map system.
    :param search_string: the search string that the nominatim server should run.
    :return: if a entity is found a polygon json is returned else None.
    """
    #TODO i think we can run a for loop in the results in case their is more then one.
    url = NOMINATIM + search_string + NOMINATIM_FORMAT
    result = requests.get(url)

    data = json.loads(result.text)

    if len(data) == 0:
        return None  # their were no results from the nominatim server.
    data = data[0]

    if data['geojson'] and data['osm_type'] == 'relation':
        polygon = data['geojson']
        return polygon  # found a hit
    else:
        return None  # the search results didn't come up with a entity.


def get_entity_polygon(entity):
    """
    this is a caller function which sends a search request to the muni finder. and iterates on all search strings.
    if found a match it will return a entity geojson feature. o
    this funciton will print the search results which were found and not found.
    A file with all entitys not found will be proccesed in the higher level.
    :param entity: the entity which is searched for in the GIS databases
    :return: True if found and added the feature to the object , False otherwise.
    """
    for name in entity.search_list:
        polygon = get_geojson_for_muni(name)
        if polygon:
            print '****************** found : ' + name + '*********************************'

            entity.add_polygon(polygon)
            return True
        else:
            print '******************** did not find ************    ' + name + '  ********** '

    return False


def create_features_for_entites(entity_list):
    for entity in entity_list:
        properties = {'name_en': entity.name_en, 'id': entity.id, 'code': entity.code,
                          'division_id' : entity.division_id,
                          'copyright': 'ODBL , http://www.openstreetmap.org/copyright'}
        feature = make_feature(entity.polygon, properties)
        entity.add_geojson_feature(feature)



def get_district_and_muni(url, entity_list):
    """
    This is the district and muni finder main() . it searchs a url from the open-muni API for all results and finds all
    Gis data it can find using these results.
    :param url: the url which is the lookup for all muni's in the open-muni API
    :param entity_list: the entity_list this is mostly here because of the recursive behivior of the function.
    :return: returns a entity dictionary which has all entity's found and all which aren't.
    """
    print url
    data = tools.get_data_as_dict(url)
    next_page = ''
    if data['next']:
        next_page = data['next']
    results_list = data['results']
    for result in results_list:
        if not result['name_en']:
            #TODO add support for results with no english keyword
            continue  # if their is no name in english. i can't store the files for now so continue.
        entity = objects.entity(result)
        if get_entity_polygon(entity):
            entity_list['found'].append(entity)  # if found add to the entity list
        else:
            entity_list['not_found'].append(entity)
    if next_page:
        get_district_and_muni(next_page, entity_list)
    return entity_list


def write_entities_to_file(entity_list):
    """
    Write all entites from a list of entity objects to file.
    the file which the entity will be writen to is depended on the file path and parent's name of the entity.
    i.e each muni , if the muni has a district the muni will be placed under the district.
    :param entity_list: the entity list to add to folders and files.
    """
    print 'writing ' + str(len(entity_list)) + ' to file'
    for entity in entity_list:
        write_to_file(entity.parent_path, entity.name_en, entity.geojson)


def write_entities_to_israel_map(entity_list):
    """
    write all entities which belong to israel into a big Map of israel.
    :param entity_list: the entity list to add to the big map.
    """
    geojson = {'type': 'FeatureCollection', 'features': []}
    for entity in entity_list:
        if entity.geojson['properties']['id'] == 11:
            continue
        geojson['features'].append(entity.geojson)

    f = open('/home/kobi/projects/open_gis/the_map/THEMAP.geojson', 'w+')
    json.dump(geojson, f)

###############################        driver :    ####################################

# i pickle the information since i don't want all data to be lost i their is an I.O Error.
# this is mostly because i wanted to get the GIS , and then write to file as a different proccess
# could be changed in the future.

entity_list = get_district_and_muni(API + VERSION + ENTITIES + '?domains=1', {'found': [], 'not_found': []})

pickle.dump(entity_list, open('/home/kobi/projects/open_gis/testing/entity_list_pickle2', 'wb'))

entity_list = pickle.load(open('/home/kobi/projects/open_gis/testing/entity_list_pickle2', 'rb'))

create_features_for_entites(entity_list['found']) # create features for all the entites found.
print 'amount found : ' + str(len(entity_list['found']))
print 'amount not found : ' + str(len(entity_list['not_found']))

write_entities_to_israel_map(entity_list['found'])
write_entities_to_file(entity_list['found'])
