#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#

from aws_cdk import (
    aws_ec2 as ec2,
    NestedStack
)
from constructs import Construct

class VpcStack(NestedStack):
    def __init__(
        self, scope: Construct, construct_id: str, cidr=None, env=None, **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            id="MWAA-End2EndDevOpsDemo--VPC",
            ip_addresses=ec2.IpAddresses.cidr("10.192.0.0/16"),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", cidr_mask=24,
                    reserved=False, subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(
                    name="private", cidr_mask=24,
                    reserved=False, subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
            ],
            enable_dns_hostnames=True,
            enable_dns_support=True
        )
