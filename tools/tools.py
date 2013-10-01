__author__ = 'kobi'

import requests
import json


################## END_POINTS  #################################:
NAME = 'name_en'
PARENT = 'parent'
###############################################################


def get_data_as_dict(url):
    """
    Get data from a URL as a python dictionary
    :param url: the url which a request is sent to.
    :return: The python dictionary data.
    """
    print url
    result = requests.get(url)
    data = json.loads(result.text)
    return data


def get_parent_path_recursive(path, result):
    """
    get the parent paths and names recursively. this is a recursive function.
    the function back traces all parents in the api and returns all a parent path.

    :param path: the path
    :param result: the resulted path
    :return: a complete path recursive
    """
    if result[PARENT] is None:
        return result[NAME]
    path = get_parent_path(path,get_data_as_dict(result[PARENT]['url'])) + '/' +result[NAME]
    return path

def get_parent_path(path , result):
    """
    the recursive initial call
    :param path: the folder path
    :param result: the resulted path.
    :return:the full parent path
    """
    parent_path = get_parent_path_recursive(path,result)
    parent_path.rstrip(result[NAME])
    return parent_path
