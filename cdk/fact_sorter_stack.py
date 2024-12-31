"""Add resources and config to the stack."""

from aws_cdk import Stack
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk import aws_iam as iam
from aws_cdk import aws_sqs as sqs
from constructs import Construct

from cdk.base_constructs.lambda_construct import LambdaConstruct


class FactSorterStack(Stack):
    """Create resources for Fact Sorter stack."""

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        """Create resources for Fact Sorter stack."""
        super().__init__(scope, id, **kwargs)

        fact_bus_dlq = sqs.Queue(self, "AnimalFactBusDLQ")

        fact_bus = events.EventBus(
            self,
            "AnimalFactBus",
            event_bus_name="animal_fact_bus",
            dead_letter_queue=fact_bus_dlq,
        )

        get_fact_dlq = sqs.Queue(self, "GetFactDLQ")

        get_fact_lamb = LambdaConstruct(
            self,
            "GetFactFunction",
            handler="fact_sorter.application.get_fact.handler",
            dead_letter_queue=get_fact_dlq,
            environment={"EVENT_BUS_ARN": fact_bus.event_bus_arn},
        )

        get_fact_lamb.function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"],
                resources=[fact_bus.event_bus_arn],
            )
        )

        cat_fact_dlq = sqs.Queue(self, "CatFactDLQ")

        cat_fact_lambda = LambdaConstruct(
            self,
            "CatFactFunction",
            handler="fact_sorter.application.cat_fact.handler",
            dead_letter_queue=cat_fact_dlq,
        )

        events.Rule(
            self,
            "CatFactRule",
            event_bus=fact_bus,
            event_pattern=events.EventPattern(
                source=["aws.lambda"],
                detail_type=["fact.retrieved"],
                detail={"animal_type": ["cat"]},
            ),
            targets=[targets.LambdaFunction(handler=cat_fact_lambda.function)],
        )
