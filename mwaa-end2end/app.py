#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#

#vpc setup already
#cdk deploy MWAAirflowStack -c vpcID=vpc-0fe5d94126e565558

#!/usr/bin/env python3
import os
import aws_cdk as cdk

from mwaairflow.mwaairflow_stack import MWAAirflowStack

env_EU=cdk.Environment(region="eu-west-2", account="XXXXXXXXXXX")

app = cdk.App()
MWAAirflowStack(
    app,
    "MWAAirflowStack",
    env=env_EU
    )

app.synth()
