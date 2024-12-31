from aws_cdk import App, Stack
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
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

    def test_lambda_has_iam_policy(self):
        app = App()
        stack = Stack(app, "TestStack")

        test_dlq = sqs.Queue(stack, "TestDLQ")
        test_policy = iam.PolicyStatement(
            actions=["sqs:SendMessage"],
            effect=iam.Effect.ALLOW,
            resources=["*"],
        )
        LambdaConstruct(
            stack,
            "TestLambda",
            handler="test_handler",
            dead_letter_queue=test_dlq,
            policy=[test_policy],
        )

        template = Template.from_stack(stack)
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
