import aws_cdk as core
import aws_cdk.assertions as assertions
from eventbus_learning.infrastructure.stack import EventbusLearningStack

app = core.App()
stack = EventbusLearningStack(app, "eventbus-learning")
template = assertions.Template.from_stack(stack)


class TestEventBusLearningStack:
    def test_lambda_created(self):
        template.resource_count_is("AWS::Lambda::Function", 1)

    def test_get_fact_lambda_has_correct_properties(self):
        template.has_resource_properties(
            "AWS::Lambda::Function",
            {
                "Handler": "get_fact.handler",
                "Runtime": "python3.12",
            },
        )
