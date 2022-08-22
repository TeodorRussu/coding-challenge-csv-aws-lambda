# csv_challenge
## The task
Given

data.csv
```
date_from, value_up_to_10_kwp, value_up_to_30_kwp, value_up_to_40_kwp
2019-01-01, 0.5062, 0.4962, 0.4862
2019-02-01, 0.4810, 0.4710, 0.4610
2019-03-01, 0.4570, 0.4470, 0.4370
2019-04-01, 0.4470, 0.4370, 0.4270
2019-05-01, 0.4370, 0.4270, 0.4170
2019-06-01, 0.3970, 0.3870, 0.3770
2019-07-01, 0.3870, 0.3770, 0.3670
2019-08-01, 0.3770, 0.3670, 0.3570
2019-09-01, 0.3670, 0.3570, 0.3470
```

Write a service that can use data.csv as a database (using csv package). If it makes sense add an in memory cache for caching requests and results.
Based on input parameters the service will be able to find the matching row/s and print out the result. 
The input parameter contains a list that can have 1 or more objects, if the list in the input has multiple objects the result will be the sum of the value column from each matched row.

The code can be in the same file or separated. 
Considering that we are using aws lambdas, would be nice if the code can be called as a function receiving input parameters and printing the result.


When the callback function is given one of the below inputs:
Write tests that cover main functionality.

```
params1 = {
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
}

params2 = {
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
}
```

Then the service prints out a correct result with a format that matches the format below

```
{
    "data": {
        "attributes": {
            "result": {
                "value": "0.08160",
            }
        }
    }
}
```


----


### The main application code:
code: 
[csv_challenge/tariffs_finder.py](https://github.com/TeodorRussu/csv_challenge/blob/2056969426214ea1ae609c59bc6c66c6953a8e8e/csv_challenge/tariffs_finder.py)

tests:
[tests/test_tariffs_finder.py](https://github.com/TeodorRussu/csv_challenge/blob/2056969426214ea1ae609c59bc6c66c6953a8e8e/tests/test_tariffs_finder.py)


### The AWS Lambda integration:
code:
[csv_challenge/app.py](https://github.com/TeodorRussu/csv_challenge/blob/2056969426214ea1ae609c59bc6c66c6953a8e8e/csv_challenge/app.py)

tests:
[tests/integration/test_api_gateway.py](https://github.com/TeodorRussu/csv_challenge/blob/2056969426214ea1ae609c59bc6c66c6953a8e8e/tests/integration/test_api_gateway.py)


### Live testing
The current code is deployed to AWS Lambda and can be invoked via AWS API Gateway using the following URL:
[https://7a9u0sdq0j.execute-api.us-east-1.amazonaws.com/Prod/challenge/](https://7a9u0sdq0j.execute-api.us-east-1.amazonaws.com/Prod/challenge/)
The GET request requires one query parameter: `'params'`, and its value should have the following structure:
Note: The query parameter should be URL encoded.
`{
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
                },{
                    "power": "40",
                    "date": "2019-12-22"
                },
                {
                    "value": "33",
                    "date": "2019-04-22"
                }
            ]
        }
    }
}`

![Live testing](/Users/temporaryadmin/PycharmProjects/csv_challenge/useful_files/Screenshot 2022-08-22 at 10.35.31.png)



----
The project contains source code and supporting files for a serverless application that can be deployed with the SAM CLI. It includes:

- csv_challenge - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. 

## Run and deploy the application
### To run the app using the SAM integrated with AWS Toolkit plugin:

To build and test, run and update easily the code, use the plugin AWS Toolkit.
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get started.**
* [PyCharm - community edition is enough](https://www.jetbrains.com/pycharm/download/)
* A valid AWS account where the app can be deployed
* [AWS CLI - used to generate local AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3.8 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.doc


### The application can be run and deployed locally using the intuitive UI in the IDE

Deploy a Lambda using the local code
![Deploy a Lambda using the local code](/Users/temporaryadmin/PycharmProjects/csv_challenge/useful_files/Screenshot 2022-08-21 at 17.58.43.png)
Deploy a serverless application using a CloudFormation template.yaml
![Deploy a serverless application using a CloudFormation template.yaml](/Users/temporaryadmin/PycharmProjects/csv_challenge/useful_files/Screenshot 2022-08-21 at 17.59.02.png)
Configure the local runtime for the Lambda function
![Configure the local runtime for the Lambda function](/Users/temporaryadmin/PycharmProjects/csv_challenge/useful_files/Screenshot 2022-08-21 at 17.59.47.png)



## To run the app using the SAM CLI, you need the following:
* A valid AWS account where the app can be deployed
* [AWS CLI - used to generate local AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3.8 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
csv_challenge$ sam build --use-container
```

The SAM CLI installs dependencies defined in `csv_challenge/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
csv_challenge$ sam local invoke CsvChallengeFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
csv_challenge$ sam local start-api
csv_challenge$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        CsvChallenge:
          Type: Api
          Properties:
            Path: /challenge
            Method: get
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
csv_challenge$ pip install -r tests/requirements.txt --user
# unit test
csv_challenge$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
csv_challenge$ AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name csv_challenge
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
