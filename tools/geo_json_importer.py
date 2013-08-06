# coding: utf-8
__author__ = 'kobi_luria'


import requests
import json
import objects
import os
import tools

# END_POINTS :

NOMINATIM =  'http://nominatim.openstreetmap.org/search?accept-language=en-us&q='
NOMINATIM_FORMAT = '&format=json&polygon_geojson=1&addressdetails=1'
API = 'http://api.dev.openmuni.org.il/'
VERSION = 'v1/'
ENTITIES = 'entities/'
DIR_PROJECT ='/home/kobi/projects/open_gis'
DIR = '/home/kobi/projects/open_gis/maps/test'
GEO_JSON = '.geojson'


def write_to_directory(parent_path ,name_en, json_object):
    dir_path = os.path.join(DIR ,parent_path).replace(' ','_').lower()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    path = os.path.join(dir_path,name_en+GEO_JSON).replace(' ','_').lower()
    f = open(path,'w+')
    json.dump(json_object,f)

def make_feature(json_polygon,json_properties):
    feature = {'type':'Feature','geometry':json_polygon,'properties':json_properties}
    return feature

def make_feature_collection(feature_list):
    feature_collection = {'features':feature_list}
    #TODO add a 'properties' to feature collection


def get_geojson_for_muni(search_string):
    url = NOMINATIM + search_string + NOMINATIM_FORMAT
    result  = requests.get(url)

    data = json.loads(result.text)

    if len(data) == 0:
        return None
    data = data[0]

    if data['geojson'] and data['osm_type'] == 'relation':
        polygon =  data['geojson']
        return polygon
    else:
        return None


def get_entity_polygon(entity):
    for name in entity.search_list:
            polygon = get_geojson_for_muni(name)
            if polygon:
                properties = {'name_en':entity.name_en,'id':entity.id,'code':entity.code,'copyright':'ODBL , http://www.openstreetmap.org/copyright'}
                feature = make_feature(polygon,properties)
                write_to_directory(entity.parent_path,entity.name_en,feature)
                return True
            else:
                print '******************** didnot find ************    ' + name +'  ********** '

    return False
def get_district_and_muni(url,count):
    data = tools.get_data_as_dict(url)
    next_page = ''
    if data['next']:
        next_page = data['next']

    results_list = data['results']
    for result in results_list:
        if not result['name_en']:
            #TODO add support for results with no english keyword
            continue # if their is no name in english. i can't store the files for now so continue.
        entity = objects.entity(result)
        if get_entity_polygon(entity):
            count += 1        # if found add the count of found
    if next_page:
        get_district_and_muni(next_page,count)
    return count


#driver :

count = get_district_and_muni(API+VERSION+ENTITIES+'?domains',0)
print count


#get_geojson_for_muni('israel')