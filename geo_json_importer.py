__author__ = 'kobi_luria'

import requests
import json
import simplejson
from simplejson import decoder

def get_geojson_for_muni(search_string):

    f = open('/test.geojson','w+')


    url = 'http://nominatim.openstreetmap.org/search?accept-language=en-us&q=' + search_string +\
          '&format=json&polygon_geojson=1&addressdetails=1'

    result  = requests.get(url)

    data = json.loads(result.text)

    data = data[0]

    if data.has_key('geojson'):
        polygon =  data.get('geojson')

        json.dump(polygon,f)


    f.close()

get_geojson_for_muni('israel')