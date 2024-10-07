import aws_cdk as core
import aws_cdk.assertions as assertions
from eventbus_learning.infrastructure.stack import EventbusLearningStack

app = core.App()
stack = EventbusLearningStack(app, "eventbus-learning")
template = assertions.Template.from_stack(stack)


class TestEventBusLearningStack:
    def test_lambda_created(self):
        template.resource_count_is("AWS::Lambda::Function", 1)
