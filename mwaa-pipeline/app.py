# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#!/usr/bin/env python3

import aws_cdk as cdk 

from mwaa_pipeline.MWAAPipeline import MWAAPipeline

env=cdk.Environment(region="eu-west-2", account="XXXXXXXXXXX")
airflow_props = {'code_repo_name': 'mwaa-dags','branch_name' : 'main', 'dags_s3_bucket_name' : 'mwaa-094459-devops-demo-dev'}


app = cdk.App()

mwaa_cicd_pipeline = MWAAPipeline(
    scope=app,
    id="mwaa-pipeline",
    env=env,
    airflow_props=airflow_props
)

app.synth()
