import csv
import datetime
import json
import re
from bisect import bisect

DATA_CSV_PATH = 'data.csv'


def find_tariffs(input_data):
    data_dict = init_db_data(DATA_CSV_PATH)
    data_dict_keys = sorted(data_dict.keys())

    input_list = input_data.get('data').get('attributes').get('list')
    result = 0
    for entry in input_list:
        date = find_date_in_the_input_item(entry)
        matching_db_date = get_the_matching_date_from_db(date, data_dict_keys)
        power = find_power_value_in_the_input_item(entry)
        tariffs = data_dict.get(matching_db_date)
        tarrif = find_matching_tarrif_from_row(power, tariffs)
        result = result + tarrif
    return result


def find_date_in_the_input_item(entry):
    date = entry.get('date')
    if not date:
        raise InputException(f'date field is missing in entry: {entry}')
    return date


def find_power_value_in_the_input_item(entry):
    power_value = entry.get('power')
    if not power_value:
        power_value = entry.get('value')
    if not power_value:
        raise InputException(f'power value field is missing or defined incorrectly in the entry: {entry}')
    power = int(power_value)
    return power


def find_matching_tarrif_from_row(power, tarrifs):
    matching_value = None
    matching_column = None

    for key in tarrifs.keys():
        if not re.match(r'value_up_to_\d*_kwp', key):
            continue

        simplified_key = int(re.sub('\D', '', key))
        if matching_value is None and simplified_key >= power:
            matching_value = simplified_key
            matching_column = key
        if matching_value is not None and power <= simplified_key < matching_value:
            matching_value = simplified_key
            matching_column = key

    if not matching_column:
        raise TariffException(message=f'Tariff not available for power {power}')
    return float(tarrifs.get(matching_column))


def find_matching_db_date(date, data_dict_keys):
    last_db_date = data_dict_keys[len(data_dict_keys) - 1]
    date_is_at_least_one_month_above_the_latest_db_date = date.year > last_db_date.year or date.month > last_db_date.month

    potential_position = bisect(data_dict_keys, date)
    if potential_position == 0:
        raise TariffException(f'Tariff not available for {datetime.datetime.strftime(date, "%Y-%m-%d")}')
    return data_dict_keys[potential_position - 1]


def get_the_matching_date_from_db(input_date, data_dict_keys):
    date = datetime.datetime.strptime(input_date, '%Y-%m-%d')
    return find_matching_db_date(date, data_dict_keys)


def init_db_data(path):
    data_dict = {}
    csv_file = open(path)
    csv_reader = csv.DictReader(csv_file)
    print('parsing the data file')
    for row in csv_reader:
        json_row = json.loads(json.dumps(row))
        for key, val in json_row.items():

            if key == 'date_from':
                date = datetime.datetime.strptime(val, '%Y-%m-%d')
                data_dict[date] = json_row
                break
    return data_dict


class TariffException(Exception):
    def __init__(self, message):
        self.message = message


class InputException(Exception):
    def __init__(self, message):
        self.message = message


class MissingInputException(Exception):
    def __init__(self, message):
        self.message = message
