"""Add resources and config to the stack."""

from aws_cdk import Stack
from aws_cdk import aws_events as events
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class EventBusLearningStack(Stack):
    """Create resources for eventbus-learning stack."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Create resources for eventbus-learning stack."""
        super().__init__(scope, construct_id, **kwargs)

        dlq = sqs.Queue(self, "GetFactDLQ")

        lambda_.Function(
            self,
            "GetFactFunction",
            code=lambda_.Code.from_asset("package.zip"),
            dead_letter_queue=dlq,
            handler="get_fact.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
        )

        fact_bus = events.EventBus(
            self, "AnimalFactBus", event_bus_name="animal_fact_bus"
        )

        events.Rule(
            self,
            "AnimalFactRule",
            event_bus=fact_bus,
            event_pattern=events.EventPattern(
                source=["aws.lambda"],
            ),
        )
