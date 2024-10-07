"""Add resources and config to the stack."""

from aws_cdk import Stack
from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class EventbusLearningStack(Stack):
    """Create resources for eventbus-learning stack."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Create resources for eventbus-learning stack."""
        super().__init__(scope, construct_id, **kwargs)

        lambda_.Function(
            self,
            "GetFactFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="get_fact.handler",
            code=lambda_.Code.from_asset("eventbus_learning/application"),
        )
