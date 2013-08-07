__author__ = 'kobi'

import tools

PARENT = 'parent'
DIVISION = 'division'
URL = 'url'
NAME_EN = 'name_en'
DISTRICT_ID = 2



class entity:

    def add_info(self,api_result):

        if(api_result[PARENT]):
            self.parent_path = tools.get_parent_path('',api_result)


        if(api_result[DIVISION]) :
            self.division_name = tools.get_data_as_dict(api_result[DIVISION][URL])['name']
            self.division_id = api_result[DIVISION]['id']

    def create_search_list(self,api_result,search_list):

        for field in search_list:
            if api_result[field]:
                if self.division_id == DISTRICT_ID:
                    self.search_list.append(api_result[field] + ' district , Israel')
                else  :
                    self.search_list.append(api_result[field] + ' , Israel')

    def add_geojson_feature(self,feature):
        self.geojson = feature

    def __init__(self,api_result):
        self.geojson = ''
        self.name_en = api_result[NAME_EN]
        self.code = api_result['code']
        self.search_list = []
        self.id = api_result['id']
        self.parent_path = ''
        self.add_info(api_result)
        self.create_search_list(api_result ,['name_en','name','name_ru','name_ar'])
