from aws_cdk import App
from aws_cdk.assertions import Capture, Template
from cdk.fact_sorter_stack import FactSorterStack

from .factories import iam_role_properties, lambda_properties

app = App()
stack = FactSorterStack(app, "fact-sorter")
template = Template.from_stack(stack)


class TestFactSorterStack:
    def test_resources_created(self):
        template.resource_count_is("AWS::Lambda::Function", 3)
        template.resource_count_is("AWS::Events::EventBus", 1)
        template.resource_count_is("AWS::Events::Rule", 2)
        template.resource_count_is("AWS::SQS::Queue", 4)


class TestGetFactLambda:
    def test_lambda_has_correct_properties(self):
        dependency_capture = Capture()
        dlq = template.find_resources("AWS::SQS::Queue").keys()
        event_bus_arn = template.find_resources("AWS::Events::EventBus").keys()
        template.has_resource_properties(
            "AWS::Lambda::Function",
            lambda_properties(
                "fact_sorter.application.get_fact.handler",
                dependency_capture,
                list(dlq)[1],
                list(event_bus_arn)[0],
            ),
        )

        assert "GetFactFunctionServiceRole" in dependency_capture.as_string()
        assert "GetFactDLQ" in list(dlq)[1]

    def test_lambda_has_correct_iam_role(self):
        role_capture = Capture()
        role = template.find_resources("AWS::IAM::Role").keys()
        template.has_resource_properties(
            "AWS::IAM::Role", iam_role_properties(role_capture)
        )

        assert "AWSLambdaBasicExecutionRole" in role_capture.as_string()
        assert "GetFactFunctionServiceRole" in list(role)[0]

    def test_lambda_has_correct_policy(self):
        policy_capture = Capture()
        role = template.find_resources("AWS::IAM::Role").keys()
        policy = template.find_resources("AWS::IAM::Policy").keys()
        template.has_resource_properties(
            "AWS::IAM::Policy",
            {
                "PolicyDocument": policy_capture,
                "PolicyName": list(policy)[0],
                "Roles": [{"Ref": list(role)[0]}],
            },
        )


class TestEventbus:
    def test_eventbus_has_correct_properties(self):
        dlq = template.find_resources("AWS::SQS::Queue").keys()
        template.has_resource_properties(
            "AWS::Events::EventBus",
            {
                "Name": "animal_fact_bus",
                "DeadLetterConfig": {
                    "Arn": {"Fn::GetAtt": [list(dlq)[0], "Arn"]}
                },
            },
        )

        assert "AnimalFactBusDLQ" in list(dlq)[0]

    def test_eventbus_cat_fact_rule_has_correct_properties(self):
        event_bus = template.find_resources("AWS::Events::EventBus").keys()
        cat_fact_func = template.find_resources("AWS::Lambda::Function").keys()
        template.has_resource_properties(
            "AWS::Events::Rule",
            {
                "EventBusName": {"Ref": list(event_bus)[0]},
                "EventPattern": {
                    "detail": {"animal": ["cat"]},
                    "detail-type": ["fact.retrieved"],
                    "source": ["GetFactFunction"],
                },
                "State": "ENABLED",
                "Targets": [
                    {
                        "Arn": {"Fn::GetAtt": [list(cat_fact_func)[1], "Arn"]},
                        "Id": "Target0",
                    }
                ],
            },
        )

    def test_eventbus_dog_fact_rule_has_correct_properties(self):
        event_bus = template.find_resources("AWS::Events::EventBus").keys()
        dog_fact_func = template.find_resources("AWS::Lambda::Function").keys()
        template.has_resource_properties(
            "AWS::Events::Rule",
            {
                "EventBusName": {"Ref": list(event_bus)[0]},
                "EventPattern": {
                    "detail": {"animal": ["dog"]},
                    "detail-type": ["fact.retrieved"],
                    "source": ["GetFactFunction"],
                },
                "State": "ENABLED",
                "Targets": [
                    {
                        "Arn": {"Fn::GetAtt": [list(dog_fact_func)[2], "Arn"]},
                        "Id": "Target0",
                    }
                ],
            },
        )


class TestCatFactLambda:
    def test_lambda_has_correct_properties(self):
        dependency_capture = Capture()
        dlq = template.find_resources("AWS::SQS::Queue").keys()
        template.has_resource_properties(
            "AWS::Lambda::Function",
            lambda_properties(
                "fact_sorter.application.cat_fact.handler",
                dependency_capture,
                list(dlq)[2],
            ),
        )

        assert "CatFactFunctionServiceRole" in dependency_capture.as_string()
        assert "CatFactDLQ" in list(dlq)[2]

    def test_lambda_has_correct_iam_role(self):
        role_capture = Capture()
        role = template.find_resources("AWS::IAM::Role").keys()
        template.has_resource_properties(
            "AWS::IAM::Role", iam_role_properties(role_capture)
        )

        assert "AWSLambdaBasicExecutionRole" in role_capture.as_string()
        assert "CatFactFunctionServiceRole" in list(role)[1]


class TestDogFactLambda:
    def test_lambda_has_correct_properties(self):
        dependency_capture = Capture()
        dlq = template.find_resources("AWS::SQS::Queue").keys()
        template.has_resource_properties(
            "AWS::Lambda::Function",
            lambda_properties(
                "fact_sorter.application.dog_fact.handler",
                dependency_capture,
                list(dlq)[3],
            ),
        )

        assert "DogFactFunctionServiceRole" in dependency_capture.as_string()
        assert "DogFactDLQ" in list(dlq)[3]

    def test_lambda_has_correct_iam_role(self):
        role_capture = Capture()
        role = template.find_resources("AWS::IAM::Role").keys()
        template.has_resource_properties(
            "AWS::IAM::Role", iam_role_properties(role_capture)
        )

        assert "AWSLambdaBasicExecutionRole" in role_capture.as_string()
        assert "DogFactFunctionServiceRole" in list(role)[2]
