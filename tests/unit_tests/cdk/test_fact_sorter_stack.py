from aws_cdk import App
from aws_cdk.assertions import Capture, Template
from cdk.fact_sorter_stack import FactSorterStack

from .factories import iam_role_properties, lambda_properties

app = App()
stack = FactSorterStack(app, "fact-sorter")
template = Template.from_stack(stack)


class TestFactSorterStack:
    def test_resources_created(self):
        template.resource_count_is("AWS::Lambda::Function", 2)
        template.resource_count_is("AWS::Events::EventBus", 1)
        template.resource_count_is("AWS::Events::Rule", 1)
        template.resource_count_is("AWS::SQS::Queue", 1)


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
                list(dlq)[0],
                list(event_bus_arn)[0],
            ),
        )

        assert "GetFactFunctionServiceRole" in dependency_capture.as_string()
        assert "GetFactDLQ" in list(dlq)[0]

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
        template.has_resource_properties(
            "AWS::Events::EventBus",
            {
                "Name": "animal_fact_bus",
            },
        )

    def test_eventbus_rule_has_correct_properties(self):
        event_bus = template.find_resources("AWS::Events::EventBus").keys()
        template.has_resource_properties(
            "AWS::Events::Rule",
            {
                "EventBusName": {"Ref": list(event_bus)[0]},
                "EventPattern": {"source": ["aws.lambda"]},
                "State": "ENABLED",
            },
        )


class TestCatFactLambda:
    def test_lambda_has_correct_properties(self):
        dependency_capture = Capture()
        template.has_resource_properties(
            "AWS::Lambda::Function",
            lambda_properties(
                "fact_sorter.application.cat_fact.handler",
                dependency_capture,
            ),
        )

        assert "CatFactFunctionServiceRole" in dependency_capture.as_string()

    def test_lambda_has_correct_iam_role(self):
        role_capture = Capture()
        role = template.find_resources("AWS::IAM::Role").keys()
        template.has_resource_properties(
            "AWS::IAM::Role", iam_role_properties(role_capture)
        )

        assert "AWSLambdaBasicExecutionRole" in role_capture.as_string()
        assert "CatFactFunctionServiceRole" in list(role)[1]
