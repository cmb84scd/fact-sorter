"""Add resources and config to the stack."""

from aws_cdk import Stack
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class FactSorterStack(Stack):
    """Create resources for Fact Sorter stack."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Create resources for Fact Sorter stack."""
        super().__init__(scope, construct_id, **kwargs)

        get_fact_dlq = sqs.Queue(self, "GetFactDLQ")

        fact_bus = events.EventBus(
            self, "AnimalFactBus", event_bus_name="animal_fact_bus"
        )

        get_fact_lambda = lambda_.Function(
            self,
            "GetFactFunction",
            code=lambda_.Code.from_asset("package"),
            dead_letter_queue=get_fact_dlq,
            handler="fact_sorter.application.get_fact.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            environment={"EVENT_BUS_ARN": fact_bus.event_bus_arn},
        )

        get_fact_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"],
                resources=[fact_bus.event_bus_arn],
            )
        )

        events.Rule(
            self,
            "AnimalFactRule",
            event_bus=fact_bus,
            event_pattern=events.EventPattern(
                source=["aws.lambda"],
            ),
        )

        lambda_.Function(
            self,
            "CatFactFunction",
            code=lambda_.Code.from_asset("package"),
            handler="fact_sorter.application.cat_fact.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
        )
