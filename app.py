#!/usr/bin/env python3
"""Create the eventbus-learning stack."""

import os

import aws_cdk as cdk
from cdk.eb_learning_stack import EventBusLearningStack

app = cdk.App()
EventBusLearningStack(
    app,
    "EventBusLearningStack",
    env=cdk.Environment(
        account=os.environ["AWS_ACCOUNT_ID"], region=os.environ["AWS_REGION"]
    ),
)

app.synth()
