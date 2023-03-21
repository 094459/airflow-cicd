# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#!/usr/bin/env python3

import aws_cdk as cdk 

from mwaa_cdk.mwaa_cdk_vpc import MwaaCdkStackVPC
from mwaa_cdk.mwaa_cdk_dev_env import MwaaCdkStackDevEnv
from mwaa_cdk.mwaa_cdk_prd_env import MwaaCdkStackPrdEnv

env_EU=cdk.Environment(region="eu-west-2", account="XXXXXXXXXXX")
mwaa_props = {'dagss3location': 'mwaa-094459-devops-demo','mwaa_env' : 'mwaa-devops-demo', 'mwaa_secrets_var':'airflow/variables', 'mwaa_secrets_conn':'airflow/connections'}

app = cdk.App()

mwaa_devopswld_vpc = MwaaCdkStackVPC(
    scope=app,
    id="mwaa-devops-vpc",
    env=env_EU,
    mwaa_props=mwaa_props
)

mwaa_devopswld_env_dev = MwaaCdkStackDevEnv(
    scope=app,
    id="mwaa-devops-dev-environment",
    vpc=mwaa_devopswld_vpc.vpc,
    env=env_EU,
    mwaa_props=mwaa_props
)

#mwaa_devopswld_env_prd = MwaaCdkStackPrdEnv(
#    scope=app,
#    id="mwaa-devopswld-prd-environment",
#    vpc=mwaa_devopswld_backend.vpc,
#    env=env_EU,
#    mwaa_props=mwaa_props
#)

app.synth()
