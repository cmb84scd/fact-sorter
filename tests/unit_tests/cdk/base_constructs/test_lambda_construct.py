import pytest
from aws_cdk import App, Stack
from aws_cdk import aws_events as events
from aws_cdk import aws_sqs as sqs
from aws_cdk.assertions import Capture, Template
from cdk.base_constructs.lambda_construct import LambdaConstruct

from ..factories import lambda_properties


class TestLambdaConstruct:
    def test_lambda_has_required_properties(self):
        app = App()
        stack = Stack(app, "TestStack")

        test_dlq = sqs.Queue(stack, "TestDLQ")
        LambdaConstruct(
            stack,
            "TestLambda",
            handler="test_handler",
            dead_letter_queue=test_dlq,
        )

        template = Template.from_stack(stack)
        dependency_capture = Capture()
        dlq = template.find_resources("AWS::SQS::Queue").keys()
        template.has_resource_properties(
            "AWS::Lambda::Function",
            lambda_properties(
                "test_handler", dependency_capture, list(dlq)[0]
            ),
        )

    def test_lambda_has_environment_variable(self):
        app = App()
        stack = Stack(app, "TestStack")

        test_bus = events.EventBus(stack, "TestBus")
        test_dlq = sqs.Queue(stack, "TestDLQ")
        LambdaConstruct(
            stack,
            "TestLambda",
            handler="test_handler",
            dead_letter_queue=test_dlq,
            environment={"EVENT_BUS_ARN": test_bus.event_bus_arn},
        )

        template = Template.from_stack(stack)
        dependency_capture = Capture()
        dlq = template.find_resources("AWS::SQS::Queue").keys()
        event_bus_arn = template.find_resources("AWS::Events::EventBus").keys()
        template.has_resource_properties(
            "AWS::Lambda::Function",
            lambda_properties(
                "test_handler",
                dependency_capture,
                list(dlq)[0],
                list(event_bus_arn)[0],
            ),
        )

    def test_construct_errors_when_required_params_are_missing(self):
        app = App()
        stack = Stack(app, "TestStack")

        expected_message = (
            r"LambdaConstruct.__init__\(\) missing 2 required positional "
            r"arguments: 'handler' and 'dead_letter_queue'"
        )

        with pytest.raises(TypeError, match=expected_message):
            LambdaConstruct(
                stack,
                "TestLambda",
            )
