import json
import os
from unittest import TestCase

import boto3
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
Make sure the correct env AWS_PROFILE pointing to the testing AWS account exists. 
"""


class TestApiGateway(TestCase):
    api_endpoint: str

    @classmethod
    def get_stack_name(cls) -> str:
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")
        if not stack_name:
            raise Exception(
                "Cannot find env var AWS_SAM_STACK_NAME. \n"
                "Please setup this environment variable with the stack name where we are running integration tests."
            )

        return stack_name

    def setUp(self) -> None:
        """
        Based on the provided env variable AWS_SAM_STACK_NAME,
        here we use cloudformation API to find out what the HelloWorldApi URL is
        """
        stack_name = TestApiGateway.get_stack_name()

        client = boto3.client("cloudformation", region_name='us-east-1')

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name}. \n" f'Please make sure stack with the name "{stack_name}" exists.'
            ) from e

        stacks = response["Stacks"]

        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "CsvChallengeApi"]
        self.assertTrue(api_outputs, f"Cannot find output CsvChallengeApi in stack {stack_name}")

        self.api_endpoint = api_outputs[0]["OutputValue"]

    def test_api_gateway__happy_flow(self):
        """
        Call the API Gateway endpoint and check the response
        """
        function_query_param = '''{
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
        }'''

        params = {'params': function_query_param}
        response = requests.get(self.api_endpoint, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'output': 0.5062})

    def test_api_gateway__happy_flow_list_as_input(self):
        """
        Call the API Gateway endpoint and check the response
        """
        function_query_param = '''{
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
            }'''

        params = {'params': function_query_param}
        response = requests.get(self.api_endpoint, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'output': 0.9772})

    def test_api_gateway_empty_input(self):
        function_query_param_blank = {"params": ""}
        response = requests.get(self.api_endpoint, params=function_query_param_blank)
        expected_output = '{"error": "The params entry has not a valid value", "input_param": {"params": ""}}'

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), json.loads(expected_output))

    def test_api_gateway_null_input(self):
        function_query_param_null = {"params": None}
        response = requests.get(self.api_endpoint, params=function_query_param_null)
        self.assertEqual(response.status_code, 400)

    def test_api_gateway__not_json_format_input(self):
        query_param = {"params": 1}
        response = requests.get(self.api_endpoint, params=query_param)
        self.assertEqual(response.status_code, 400)

    def test_api_gateway__input_valid_format__corrupted_data(self):
        """
        Call the API Gateway endpoint and check the response
        """
        function_query_param = '''{
                "data": {
                    "attributes": {
                        "list": [
                            {
                                "invalid_power": "12",
                                "date": "2019-01-22"
                            },
                            {
                                "value": "8",
                                "date": "2019-02-22"
                            }
                        ]
                    }
                }
            }'''

        expected_output = '''
            {
              "error": "power value field is missing or defined incorrectly in the entry: {'invalid_power': '12', 'date': '2019-01-22'}",
              "input_param": {
                "data": {
                  "attributes": {
                    "list": [
                      {
                        "invalid_power": "12",
                        "date": "2019-01-22"
                      },
                      {
                        "value": "8",
                        "date": "2019-02-22"
                      }
                    ]
                  }
                }
              }
            }
        '''

        params = {'params': function_query_param}
        response = requests.get(self.api_endpoint, params=params)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), json.loads(expected_output))
