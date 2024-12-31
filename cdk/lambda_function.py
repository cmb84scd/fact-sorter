"""Construct for an AWS Lambda Function."""

from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class LambdaConstruct(Construct):
    """AWS base lambda construct."""

    def __init__(
        self,
        scope: Construct,
        id: str,
        handler: str,
        dead_letter_queue: str,
        environment: dict = None,
        policy: list = None,
        **kwargs,
    ) -> None:
        """AWS base lambda construct."""
        super().__init__(scope, id, **kwargs)

        base_lambda = lambda_.Function(
            self,
            id,
            code=lambda_.Code.from_asset("package"),
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler=handler,
            dead_letter_queue=dead_letter_queue,
        )

        if environment is not None:
            for k, v in environment.items():
                base_lambda.add_environment(k, v)

        if policy is not None:
            for p in policy:
                base_lambda.add_to_role_policy(p)