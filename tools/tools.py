__author__ = 'kobi'

import requests
import json

NAME = 'name_en'
PARENT = 'parent'
def get_data_as_dict(url):
    result = requests.get(url)
    data = json.loads(result.text)
    return data


def get_parent_path_recursive(path ,result):
    if result[PARENT] == None:
        return result[NAME]
    path = get_parent_path(path,get_data_as_dict(result[PARENT]['url'])) + '/' +result[NAME]
    return path

def get_parent_path(path , result):
    parent_path = get_parent_path_recursive(path,result)
    parent_path.rstrip(result[NAME])
    return parent_path

