__author__ = 'kobi'

import tools

################## END_POINTS  #################################:
PARENT = 'parent'
DIVISION = 'division'
URL = 'url'
NAME_EN = 'name_en'
DISTRICT_ID = 2
#################################################################


class entity:
    """
    A class which represents an entity and has GIS info and open-muni info within it.
    """
    def add_info(self, api_result):

        """
        add info which isn't given directly by the muni - API , we search for the path untill the highest parent and
        add the division name.
        :type api_result: an API result from open muni
        :param api_result: the Api search result for this entity.
        """
        if api_result[PARENT]:
            self.parent_path = tools.get_parent_path('', api_result)

        if api_result[DIVISION]:
            self.division_name = tools.get_data_as_dict(api_result[DIVISION][URL])['name']
            self.division_id = api_result[DIVISION]['id']

    def create_search_list(self, api_result, search_list):
        """
        create a search list which is updated to current demands ,
        currently adds a 'district' string to district search , and israel to all
        :param api_result: the API result of this entity.
        :param search_list: The search list includes ***** field names from the API ******
        :return:this funciton currently just appends the search list to an object.
        """

        for field in search_list:
            if api_result[field]:
                if self.division_id == DISTRICT_ID:
                    self.search_list.append(api_result[field] + ' district , Israel')
                else:
                    self.search_list.append(api_result[field] + ' , Israel')

    def add_geojson_feature(self, feature):
        """
        A set function for the geojson feature of this object.
        :param feature: the geojson feature which belongs to this entity.
        :return: None
        """
        self.geojson = feature


    def add_polygon(self,polygon):
        self.polygon = polygon

    def __init__(self, api_result):
        """
        Init for an entity object. starts up all fields and updated the simple ones directly from th api_reslut.
        :param api_result : an open muni API call results which is the result for this muni.
        :return: None
        """
        self.geojson = ''
        self.polygon = ''
        self.name_en = api_result[NAME_EN]
        self.code = api_result['code']
        self.search_list = []
        self.id = api_result['id']
        self.parent_path = ''
        self.add_info(api_result)
        self.create_search_list(api_result, ['name_en', 'name', 'name_ru', 'name_ar'])
