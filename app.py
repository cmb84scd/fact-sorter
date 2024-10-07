#!/usr/bin/env python3
"""Create the eventbus-learning stack."""

import aws_cdk as cdk
from eventbus_learning.infrastructure.stack import EventbusLearningStack

app = cdk.App()
EventbusLearningStack(app, "eventbus-learning")

app.synth()
