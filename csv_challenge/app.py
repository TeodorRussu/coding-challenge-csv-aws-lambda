import json

from tariffs_finder import TariffException, find_tariffs, InputException, MissingInputException


def lambda_handler(event, context):
    try:
        input_raw_data = event.get('queryStringParameters')

        if not input_raw_data:
            raise MissingInputException('The request has no query parameters')

        params_content = input_raw_data.get('params')
        if not params_content:
            raise MissingInputException('The params entry has not a valid value')

        input_payload = json.loads(params_content)
        output = find_tariffs(input_payload)

    except (TariffException, InputException) as exception:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": exception.message,
                "input_param": input_payload
            }),
        }
    except MissingInputException as exception:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": exception.message,
                "input_param": input_raw_data
            }),
        }

    except Exception as exception:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": repr(exception),
                "input_param": input_raw_data
            }),
        }
    return {
        "statusCode": 200,
        "body": json.dumps({
            "output": output,
        }),
    }
