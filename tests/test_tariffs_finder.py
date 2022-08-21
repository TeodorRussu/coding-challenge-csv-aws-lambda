import datetime
import json
from unittest import TestCase

from csv_challenge.tariffs_finder import get_the_matching_date_from_db, find_matching_tarrif_from_row, TariffException, \
    find_power_value_in_the_input_item, InputException, find_date_in_the_input_item, find_tariffs


class Test(TestCase):

    # test tariff finding against different structures of the data.csv
    def test_find_matching_tarrif_from_row__within_the_available_ranges__columns_sorted__ok(self):
        expected_output_tariff = 0.5062

        row = {'date_from': '2019-01-01', 'value_up_to_10_kwp': f'{expected_output_tariff}',
               'value_up_to_30_kwp': '0.4962',
               'value_up_to_40_kwp': '0.4862'}

        result = find_matching_tarrif_from_row(6, row)
        self.assertEqual(expected_output_tariff, result)

    def test_find_matching_tarrif_from_row__within_the_available_ranges__columns_not_sorted__ok(self):
        expected_output_tariff = 0.4862

        row = {'date_from': '2019-01-01', 'value_up_to_10_kwp': '0.5062', 'value_up_to_30_kwp': '0.4962',
               'value_up_to_7_kwp': f'{expected_output_tariff}'}

        result = find_matching_tarrif_from_row(6, row)
        self.assertEqual(expected_output_tariff, result)

    def test_find_matching_tarrif_from_row__outside_the_available_ranges__columns_sorted__exception(self):
        row = {'date_from': '2019-01-01', 'value_up_to_10_kwp': '0.5062', 'value_up_to_30_kwp': '0.4962',
               'value_up_to_40_kwp': '0.4862'}

        with self.assertRaises(TariffException) as context:
            find_matching_tarrif_from_row(50, row)

        self.assertTrue(f'Tariff not available for power {50}' in str(context.exception.message))

    # # test tariff finding against different date scenarios
    def test_map_the_input_date_to_db_date__within_the_available_dates_intervals_ok(self):
        test_dates = self.string_dates_to_dates_list(
            ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01'])

        expected_output = datetime.datetime.strptime("2022-01-01", '%Y-%m-%d')

        output = get_the_matching_date_from_db("2022-01-12", test_dates)
        self.assertEqual(expected_output, output)

    def test_map_the_input_date_to_db_date__later_than_available_dates_intervals__pick_the_last_item(self):
        test_dates = self.string_dates_to_dates_list(
            ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01'])

        expected_output = datetime.datetime.strptime("2022-05-01", '%Y-%m-%d')

        output = get_the_matching_date_from_db("2022-08-12", test_dates)
        self.assertEqual(expected_output, output)

    def test_map_the_input_date_to_db_date__earlier_than_available_dates_intervals__throw_exception(self):
        test_dates = self.string_dates_to_dates_list(
            ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01'])

        with self.assertRaises(TariffException) as context:
            get_the_matching_date_from_db("1999-08-12", test_dates)

        self.assertTrue('Tariff not available for 1999-08-12' in str(context.exception.message))

    # test power field in input list item
    def test_find_power_value_in_the_input_item__power_defined_as_power(self):
        expected_output = 8
        entry = json.loads('{"power": %s, "date": "2019-02-22"}' % expected_output)
        output = find_power_value_in_the_input_item(entry)

        self.assertEqual(expected_output, output)

    def test_find_power_value_in_the_input_item__power_defined_as_value(self):
        expected_output = 8
        entry = json.loads('{"value": %s, "date": "2019-02-22"}' % expected_output)
        output = find_power_value_in_the_input_item(entry)

        self.assertEqual(expected_output, output)

    def test_find_power_value_in_the_input_item__no_power_defined_as_value__exception(self):
        expected_output = 8
        entry = json.loads('{"wrong_power_key": %s, "date": "2019-02-22"}' % expected_output)

        with self.assertRaises(InputException) as context:
            find_power_value_in_the_input_item(entry)

        self.assertTrue(f'power value field is missing or defined incorrectly in the entry: {entry}' in str(
            context.exception.message))

    # test missing date field
    def test_find_power_value_in_the_input_item__no_power_defined_as_value__exception(self):
        expected_output = 8
        entry = json.loads('{"power": %s, "wrong_date_key": "2019-02-22"}' % expected_output)

        with self.assertRaises(InputException) as context:
            find_date_in_the_input_item(entry)

        self.assertTrue(f'date field is missing in entry: {entry}' in str(context.exception.message))

    # e2e logic test
    def test_find_tariffs_valid_data_file__valid_input__one_item_in_input_list(self):
        input_data = json.loads(
            '''{
                "data": {
                    "attributes": {
                        "list": [
                            {
                                "power": "6",
                                "date": "2019-01-22"
                            }
                        ]
                    }
                }
            }''')
        output = find_tariffs(input_data)
        self.assertEqual(0.5062, output)

    def test_find_tariffs_valid_data_file__valid_input__two_items_in_input_list(self):
        input_data = json.loads(
            '''{
                "data": {
                    "attributes": {
                        "list": [
                            {
                                "power": "12",
                                "date": "2019-01-22"
                            },
                            {
                                "value": "8",
                                "date": "2019-02-22"
                            }
                        ]
                    }
                }
            }''')
        output = find_tariffs(input_data)
        self.assertEqual(0.9772, output)

    def string_dates_to_dates_list(self, dates):
        dates_list = []
        for date in dates:
            dates_list.append(datetime.datetime.strptime(date, '%Y-%m-%d'))
        return dates_list
