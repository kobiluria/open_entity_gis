# coding: utf-8
import fetch
import unicode_csv

__author__ = 'kobi'

import time
import sys


def parse_csv_to_municipalities(csv_to_be_parsed, csv_parsed_successfully, csv_parsed_unsuccessfully, format="kml",
                                search_column=0):
    """
    A tool to parse a csv file into a csv which contains the municipalities boundaries
    The tool will parse search_column and find the boundaries of a municipality.

    this tool uses open_street_map

    One column of csv to be parsed should contain the name of the muni to be search for.
    Another

    csv_to_be_parsed = file to be parsed
    csv_parsed_successfully = file name to write successfull search which found a muni boundry polygon
    csv_parsed_unsuccessfully =  file name write all search csv lines which didn't find a muni boundry match.
    format = the format of the column which will contain the polygon's of the muni boundry
    search_column = the column which contains the name of the muni search for.

    """

    #TODO add a handle for formatting a different formats
    #TODO add a option for using a more complex csv
    #TODO add a option for google search

    csv_to_be_parsed = open(csv_to_be_parsed, 'rb')
    csv_parsed_successfully = open(csv_parsed_successfully, 'w+')
    csv_parsed_unsuccessfully = open(csv_parsed_unsuccessfully, 'w+')

    reader = unicode_csv.UnicodeReader(csv_to_be_parsed)
    writer_successfully = unicode_csv.UnicodeWriter(csv_parsed_successfully)
    writer_unsuccessfully = unicode_csv.UnicodeWriter(csv_parsed_unsuccessfully)
    writer_successfully.writerow(['unique_id', 'name', 'city', 'state', 'country', 'osm_id', 'lat', 'lng', 'polygon'])
    writer_unsuccessfully.writerow(['unique_id', 'name', 'city', 'state', 'country', 'osm_id', 'lat', 'lng', 'polygon'])
    search_string_1 = ''
    search_string_2 = ''
    unique_id = ''
    for row in reader:
        search_string_1 = row[1]
        search_string_2 = row[2]
        unique_id = row[0]

        time.sleep(.5)
        entity_data = fetch.get_entity_data(unique_id, search_string_1)
        if entity_data:
            print entity_data
            writer_successfully.writerow(entity_data)
        elif search_string_2:
            entity_data = fetch.get_entity_data(unique_id, search_string_2)

            if entity_data:
                print entity_data
                writer_successfully.writerow(entity_data)

            else:
                print '*************     did not find : ' + search_string_1 + ' or :' + search_string_2 + \
                      ' unique id number : ' \
                      + unique_id + '   ******************'
                writer_unsuccessfully.writerow([unique_id, search_string_1, search_string_2])


def update_csv_to_municipalities(csv_to_be_parsed, csv_parsed_successfully, csv_parsed_unsuccessfully, format="kml"):
    """

    :param csv_to_be_parsed:
    :param csv_parsed_successfully:
    :param csv_parsed_unsuccessfully:
    :param format:
    this tool uses a complete csv which has the osm_id numbers to search and reformat the csv to the complete format :


    this tool uses open_street_map


    """

    #TODO add a handle for formatting a different formats
    #TODO add a option for using a more complex csv
    #TODO add a option for google search

    csv_to_be_parsed = open(csv_to_be_parsed, 'rb')
    csv_parsed_successfully = open(csv_parsed_successfully, 'w+')
    csv_parsed_unsuccessfully = open(csv_parsed_unsuccessfully, 'w+')

    reader = unicode_csv.UnicodeReader(csv_to_be_parsed)
    writer_successfully = unicode_csv.UnicodeWriter(csv_parsed_successfully)
    writer_unsuccessfully = unicode_csv.UnicodeWriter(csv_parsed_unsuccessfully)
    writer_successfully.writerow(['unique_id', 'name', 'city', 'state', 'country', 'osm_id', 'lat', 'lng', 'polygon'])
    writer_unsuccessfully.writerow(
        ['unique_id', 'name', 'city', 'state', 'country', 'osm_id', 'lat', 'lng', 'polygon)'])

    for row in reader:
        unique_id = row[0]
        search_string = row[1]
        osm_id = row[2]

        time.sleep(.2)
        entity_data = fetch.get_entity_data_from_osm_id(unique_id, search_string, osm_id)
        if entity_data:
            print entity_data
            writer_successfully.writerow(entity_data)
        # if for some reason this id was not found on open street data
        else:
            print '*************     did not find  osm_id: ' + osm_id + 'unique id : ' + unique_id + \
                  '   ******************'
            writer_unsuccessfully.writerow([unique_id, osm_id])


def polygon_csv_to_kml(data_csv, kml_colmun, name_colmun, lat_colmun, lan_colmun, id_colmun):
    """
    A tool to parse a csv which has a polygon column into a kml file

    data_csv = a file name which contains o polygon_info in kml format and data

    name_colmun = the column number of name of kml_data in data file

    name_colmun = the column number of name of muni in data file

    lat_colmun = the column number of latitude in data file

    lan_colmun = the column number of the longitude in data file

    id_colmun =  the column number of the id in data file
    """


def add_polygon_csv_to_google_fusion_map(data_csv, google_fusion_object):
    """
    addes a polygon csv file into a google map , including all info and data.

    data_csv =  the data csv to import
    google_fusion_object = an object which is in the directory which has methods and key to update
    and import a csv to a google fusion map

    """

