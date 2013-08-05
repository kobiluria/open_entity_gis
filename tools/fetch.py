__author__ = 'kobi'
# coding: utf-8
from lxml import etree as et
#import urllib2


def get_wanted_entity(xml_element, look_up_dic=None):
    """
    default of look_up_dic should be {'osm_type':'relation'}
    get a wanted entity from an xml_element which was outputed from a nominatim server.

    the element returend will be a "place" element i.e an  xml element which has all values of a osm xml

    those involve place id , osm_type , osm_id etc.

    :param xml_element: the xml element to look up
    :param look_up_dic: a Dictionary which has pair key value to look for when finding an element
    :returns  a element , or a NONE if not found.
    :rtype : xml element tree
    """
    results = xml_element.findall("place")
    for result in results:
        for look_up in look_up_dic.iterkeys():
            if result.get(look_up) == look_up_dic[look_up]:
                return result
    return None


def get_name(element_tree):
    """
    get's a name from an "place" osm element .

    :param element_tree: a element tree to get a name from
    :returns: a name of the element
    """
    return element_tree.get('display_name')


def get_polygon_kml(element_tree):
    """
    gets a kml polygon from a "place" element
    :param element_tree: the element xml which has a polygon
    """
    geokml = element_tree.find('geokml')
    if geokml.find('MultiGeometry'):
        polygon = geokml.find('MultiGeometry').find('Polygon')
        return polygon
    polygon = geokml.find('Polygon')
    return polygon


def get_osm_id(element_tree):
    """
    gets a osm_id number from a "place" element
    """

    return element_tree.get('osm_id')


def get_latitude(element_tree):
    """
    gets a osm_latitude number from a "place" element
    """
    return element_tree.get('lat')


def get_longitude(element_tree):
    """
    gets a osm_longitude number from a "place" element
    """
    return element_tree.get('lon')


def get_city(element_tree):
    """
    gets a city name from a "place" element
    """
    city = element_tree.find('city')
    if(city is None):
        return ''
    return city.text


def get_state(element_tree):
    """
    gets a state name from a "place" element
    """
    state = element_tree.find('state')
    if(state is None):
        return ''
    return state.text


def get_country(element_tree):
    """
    gets a country name from a "place" element
    :param element_tree: 
    """
    country = element_tree.find('country')
    if country is None:
        return ''
    return country.text


def get_entity_data(unique_id, entity_name):
    """

    :param unique_id:
    :param entity_name:
    :return:
    """
    search_dic = {'osm_type': 'relation'}
    result_element = et.parse(
        'http://nominatim.openstreetmap.org/search?accept-language=en-us&q=' + entity_name +
        '&format=xml&polygon_kml=1&addressdetails=1')
    wanted_element = get_wanted_entity(result_element, search_dic)
    if wanted_element is None:
        return None
    name = get_name(wanted_element)
    osm_id = get_osm_id(wanted_element)
    lat = get_latitude(wanted_element)
    lng = get_longitude(wanted_element)
    city = get_city(wanted_element)
    state = get_state(wanted_element)
    country = get_country(wanted_element)
    polygon = get_polygon_kml(wanted_element)
    if name and osm_id and lat and lng and city and state and country and polygon is None:
        return None
    print 'this is a google polygon :', et.tostring(polygon)
    return [unique_id, name, city, state, country, osm_id, lat, lng, et.tostring(polygon)]


def get_entity_data_from_osm_id(unique_id,search_string, osm_id):
    """


    :rtype : object
    :param unique_id: 
    :param search_string: 
    :param osm_id: 
    :return: 
    """
    search_dic = {'osm_id': osm_id}
    result_element = et.parse(
        #TODO use nominatim on a usage policy see their usage policy.
        'http://nominatim.openstreetmap.org/search?accept-language=en-us&q=' + search_string +
        '&format=xml&polygon_kml=1&addressdetails=1')
    wanted_element = get_wanted_entity(result_element, search_dic)
    if wanted_element is None:
        return None
    name = get_name(wanted_element)
    osm_id = get_osm_id(wanted_element)
    lat = get_latitude(wanted_element)
    lng = get_longitude(wanted_element)
    city = get_city(wanted_element)
    state = get_state(wanted_element)
    country = get_country(wanted_element)
    polygon = get_polygon_kml(wanted_element)
    if polygon is None:
        return None

    print 'this is a google polygon :', et.tostring(polygon)
    return [unique_id, name, city, state, country, osm_id, lat, lng, et.tostring(polygon)]