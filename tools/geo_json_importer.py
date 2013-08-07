# coding: utf-8
__author__ = 'kobi_luria'


import requests
import json
import objects
import os
import tools
import pickle
# END_POINTS :

NOMINATIM =  'http://nominatim.openstreetmap.org/search?accept-language=en-us&q='
NOMINATIM_FORMAT = '&format=json&polygon_geojson=1&addressdetails=1'
API = 'http://api.dev.openmuni.org.il/'
VERSION = 'v1/'
ENTITIES = 'entities/'
DIR_PROJECT ='/home/kobi/projects/open_gis'
DIR = '/home/kobi/projects/open_gis/maps'
GEO_JSON = '.geojson'


def write_to_file(parent_path ,name_en, json_object):
    dir_path = os.path.join(DIR ,parent_path).rstrip(name_en).replace(' ','_').lower()
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
                print '****************** found : ' + name + '*********************************'
                properties = {'name_en':entity.name_en,'id':entity.id,'code':entity.code,'copyright':'ODBL , http://www.openstreetmap.org/copyright'}
                feature = make_feature(polygon,properties)
                entity.add_geojson_feature(feature)
                #write_to_directory(entity.parent_path,entity.name_en,feature)
                return True
            else:
                print '******************** didnot find ************    ' + name +'  ********** '

    return False
def get_district_and_muni(url,entity_list):
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
            entity_list['found'].append(entity) # if found add to the entity list
        else:
            entity_list['not_found'].append(entity)
    if next_page:
        get_district_and_muni(next_page,entity_list)
    return entity_list

def write_entities_to_file(entity_list):
    print 'writing ' + str(len(entity_list)) +' to file'
    for entity in entity_list:
        write_to_file(entity.parent_path,entity.name_en,entity.geojson)

def write_entities_to_israel_map(entity_list):
    geojson ={'type': 'FeatureCollection','features': []}
    for entity in entity_list:
        if entity.division_id == 1 or entity.division_id==2 :
            entity.geojson['geometry']['type']='LineString'
        geojson['features'].append(entity.geojson)

    f = open('/home/kobi/projects/open_gis/the_map/THEMAP','w+')
    json.dump(geojson,f)
#driver :

#entity_list = get_district_and_muni(API+VERSION+ENTITIES+'?domains',{'found':[],'not_found':[]})

#pickle.dump(entity_list,open('/home/kobi/projects/open_gis/testing/entity_list_pickle','wb'))

entity_list = pickle.load(open('/home/kobi/projects/open_gis/testing/entity_list_pickle','rb'))

print 'amount found : ' + str(len(entity_list['found']))
print 'amount not found : ' + str(len(entity_list['not_found']))

write_entities_to_israel_map(entity_list['found'])

write_entities_to_file(entity_list['found'])

