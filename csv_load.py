# coding: utf-8
import muni_boundaries_csv
import unicode_csv

from time import gmtime, strftime

datestring = strftime("%d%b%Y_%H%M%S", gmtime())
csvstring = '.csv'


def fix_csv(data_csv, fixed_csv):
    """ fix a csv to have an id and a open street search name
    adds israel to the search item
    :param data_csv: orignal data csv
    :param fixed_csv: the fixed data csv
    """
    reader_file = open(data_csv, 'rb')
    writer_file = open(fixed_csv, 'r+')
    reader = unicode_csv.UnicodeReader(reader_file)
    writer = unicode_csv.UnicodeWriter(writer_file)

    header = reader.next()
    print header
    for row in reader:
        open_street_search = row[3] + ' Israel'
        open_street_search_english = row[4] + ' Israel'
        print row[1], open_street_search, 'or : ', open_street_search_english
        writer.writerow([row[1], open_street_search, open_street_search_english])

    reader_file.close()
    writer_file.close()


def fix_csv_area(district_csv, fixed_csv):
    """ fix a csv to have an id and a open strat search name """
    reader_file = open(district_csv, 'rb')
    writer_file = open(fixed_csv, 'w+')
    reader = unicode_csv.UnicodeReader(reader_file)
    writer = unicode_csv.UnicodeWriter(writer_file)

    header = reader.next()
    print header
    for row in reader:
        open_street_search = row[3] + ' District' + ' Israel'
        open_street_search_english = row[4] + ' District' + ' Israel'
        if row[1] == '1111114':
            open_street_search_english = 'judea and samaria Area'
        print row[1], open_street_search, 'or : ', open_street_search_english
        writer.writerow([row[1], open_street_search, open_street_search_english])

    reader_file.close()
    writer_file.close()


#read_csv = '/home/python/PycharmProjects/omuni-budget/openbudget/apps/fmaps/static/area.csv'
#data_csv = '/home/python/PycharmProjects/omuni-budget/openbudget/apps/fmaps/static/data_' + datestring + csvstring
#succsesful_csv = '/home/python/PycharmProjects/omuni-budget/openbudget/apps/fmaps/static/succses_' + datestring + \
#                csvstring
#unsuccsesful_csv = '/home/python/PycharmProjects/omuni-budget/openbudget/apps/fmaps/static/unsuccses_' + datestring +\
#                  csvstring

idData = 'D:\DB\data.csv'
succsesful_csv = 'D:\DB\succses_' + datestring + csvstring
unsuccsesful_csv = 'D:\DB\unsuccses_' + datestring + csvstring

#fix_csv(read_csv,data_csv)
#fix_csv_area(read_csv, data_csv)
muni_boundaries_csv.update_csv_to_municipalities(idData, succsesful_csv, unsuccsesful_csv)