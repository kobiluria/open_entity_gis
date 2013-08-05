# coding: utf-8
__author__ = 'kobi_luria'


import requests
import json
import simplejson
from simplejson import decoder
import os

# END_POINTS :

NOMINATIM =  'http://nominatim.openstreetmap.org/search?accept-language=en-us&q='
NOMINATIM_FORMAT = '&format=json&polygon_geojson=1&addressdetails=1'
API = 'http://api.dev.openmuni.org.il/'
VERSION = 'v1/'
ENTITIES = 'entities/'
DIR_PROJECT ='/home/kobi/projects/open_gis'
DIR = '/home/kobi/projects/open_gis/maps/'
GEO_JSON = '.geojson'



def get_data_as_dict(url):
    result = requests.get(url)
    data = json.loads(result.text)
    return data

def write_to_directory(parent_path ,name_en, json_object):
    path = ''
    if parent_path:
        dir_path = os.path.join(DIR,parent_path.rstrip(name_en)).replace(' ','_').lower()
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path = os.path.join(dir_path,name_en+GEO_JSON).replace(' ','_').lower()
    else :
        path = os.path.join(DIR,name_en+GEO_JSON).replace(' ','_').lower()
    f = open(path,'w+')
    json.dump(json_object,f)

def make_feature(json_polygon,json_properties):
    feature = {'type':'Feature','geometry':json_polygon,'properties':json_properties}
    return feature

def make_feature_collection(feature_list):
    feature_collection = {'features':feature_list}
    #TODO add a 'properties' to feature collection


def get_parent_path(path ,result):
    if result['parent'] == None:
        return result['name_en']
    path = get_parent_path(path,get_data_as_dict(result['parent']['url'])) + '/' +result['name_en']
    return path

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



def get_district_and_muni(url,count):
    data = get_data_as_dict(url)
    next_page = ''
    if data['next']:
        next_page = data['next']

    results_list = data['results']
    for result in results_list:
        if not result['name_en']:
            #TODO add support for results with no english keyword
            continue # if their is no name in english. i can't store the files for now so continue.

        id = result['id']
        name_en = result['name_en']
        if(result['parent']):
            parent_name = get_data_as_dict(result['parent']['url'])['name']
        code = result['code']
        if(result['division']) :
            division_name = get_data_as_dict(result['division']['url'])['name']
        name_list = []

        name_list.append(result['name'] + ' ISRAEL')
        name_list.append(result['name_en'] + ' ISRAEL')

        parent_path = ''
        if(result['parent']):
            parent_path = get_parent_path('',result)
        for name in name_list:
            polygon = get_geojson_for_muni(name)
            if polygon:
                properties = {'name_en':name_en,'id':id,'code':code,'copyright':'ODBL , http://www.openstreetmap.org/copyright'}
                feature = make_feature(polygon,properties)
                write_to_directory(parent_path,name_en,feature)
                count = count + 1
                break
            else:
                print '******************** didnot find ************    ' + name_en +'  ********** '
    if(next_page):
        get_district_and_muni(next_page,count)

    return count


count = get_district_and_muni(API+VERSION+ENTITIES+'?domains',0)
print count


#get_geojson_for_muni('israel')