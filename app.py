#!/usr/bin/env python3
"""Create the Fact Sorter stack."""

import os

import aws_cdk as cdk
from cdk.fact_sorter_stack import FactSorterStack

app = cdk.App()
FactSorterStack(
    app,
    "FactSorterStack",
    env=cdk.Environment(
        account=os.environ["AWS_ACCOUNT_ID"], region=os.environ["AWS_REGION"]
    ),
)

app.synth()
