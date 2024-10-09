from aws_cdk import App
from aws_cdk.assertions import Capture, Template
from eventbus_learning.infrastructure.stack import EventbusLearningStack

app = App()
stack = EventbusLearningStack(app, "eventbus-learning")
template = Template.from_stack(stack)


class TestEventBusLearningStack:
    def test_lambda_created(self):
        template.resource_count_is("AWS::Lambda::Function", 1)

    def test_get_fact_lambda_has_correct_properties(self):
        dependency_capture = Capture()
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {
                "Handler": "get_fact.handler",
                "Role": {"Fn::GetAtt": [dependency_capture, "Arn"]},
                "Runtime": "python3.12",
            },
        )

        assert "GetFactFunctionServiceRole" in dependency_capture.as_string()
