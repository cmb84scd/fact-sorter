from aws_cdk import App
from aws_cdk.assertions import Capture, Match, Template
from eventbus_learning.infrastructure.stack import EventbusLearningStack

from ..factories import lambda_properties

app = App()
stack = EventbusLearningStack(app, "eventbus-learning")
template = Template.from_stack(stack)


class TestEventBusLearningStack:
    def test_lambda_created(self):
        template.resource_count_is("AWS::Lambda::Function", 1)

    def test_get_fact_lambda_has_correct_properties(self):
        dependency_capture = Capture()
        template.has_resource_properties(
            "AWS::Lambda::Function", lambda_properties(dependency_capture)
        )

        assert "GetFactFunctionServiceRole" in dependency_capture.as_string()

    def test_lambda_has_correct_iam_role(self):
        role_capture = Capture()
        template.has_resource_properties(
            "AWS::IAM::Role",
            {
                "AssumeRolePolicyDocument": {
                    "Statement": [
                        {
                            "Action": "sts:AssumeRole",
                            "Effect": "Allow",
                            "Principal": {"Service": "lambda.amazonaws.com"},
                        }
                    ],
                },
                "ManagedPolicyArns": [
                    {
                        "Fn::Join": Match.array_with(
                            [
                                [
                                    "arn:",
                                    {"Ref": "AWS::Partition"},
                                    role_capture,
                                ]
                            ]
                        )
                    }
                ],
            },
        )

        assert "AWSLambdaBasicExecutionRole" in role_capture.as_string()
