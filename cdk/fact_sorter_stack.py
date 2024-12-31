"""Add resources and config to the stack."""

from aws_cdk import Stack
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from aws_cdk import aws_sqs as sqs
from constructs import Construct

from cdk.lambda_function import LambdaConstruct


class FactSorterStack(Stack):
    """Create resources for Fact Sorter stack."""

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        """Create resources for Fact Sorter stack."""
        super().__init__(scope, id, **kwargs)

        fact_bus = events.EventBus(
            self, "AnimalFactBus", event_bus_name="animal_fact_bus"
        )

        get_fact_policy = iam.PolicyStatement(
            actions=["events:PutEvents"],
            resources=[fact_bus.event_bus_arn],
        )

        get_fact_dlq = sqs.Queue(self, "GetFactDLQ")

        LambdaConstruct(
            self,
            "GetFactFunction",
            handler="fact_sorter.application.get_fact.handler",
            dead_letter_queue=get_fact_dlq,
            environment={"EVENT_BUS_ARN": fact_bus.event_bus_arn},
            policy=[get_fact_policy],
        )

        events.Rule(
            self,
            "AnimalFactRule",
            event_bus=fact_bus,
            event_pattern=events.EventPattern(
                source=["aws.lambda"],
            ),
        )

        cat_fact_dlq = sqs.Queue(self, "CatFactDLQ")

        LambdaConstruct(
            self,
            "CatFactFunction",
            handler="fact_sorter.application.cat_fact.handler",
            dead_letter_queue=cat_fact_dlq,
        )
