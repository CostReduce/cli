# -*- coding: utf-8 -*-
import boto3
from moto import mock_elbv2, mock_ec2
from costreduce.core.services.aws.ec2 import Ec2


@mock_elbv2
def test_get_alb_arn_is_empty(boto3_mock):
    aws = Ec2(boto3_mock, "us-east-1")
    result = aws.get_elb_arn()
    result.should.equal([])


@mock_ec2
@mock_elbv2
def test_get_alb_arn_is_not_empty(boto3_mock):
    conn = boto3.client("elbv2", region_name="us-east-1")
    ec2 = boto3.resource("ec2", region_name="us-east-1")
    security_group = ec2.create_security_group(
        GroupName="a-security-group", Description="First One"
    )
    vpc = ec2.create_vpc(CidrBlock="172.28.7.0/24", InstanceTenancy="default")
    subnet1 = ec2.create_subnet(
        VpcId=vpc.id, CidrBlock="172.28.7.192/26", AvailabilityZone="us-east-1a"
    )
    subnet2 = ec2.create_subnet(
        VpcId=vpc.id, CidrBlock="172.28.7.0/26", AvailabilityZone="us-east-1b"
    )
    conn.create_load_balancer(
        Name="my-lb",
        Subnets=[subnet1.id, subnet2.id],
        SecurityGroups=[security_group.id],
        Scheme="internal",
        Tags=[{"Key": "key_name", "Value": "a_value"}],
    )

    aws = Ec2(boto3_mock, "us-east-1")
    result = aws.get_elb_arn()
    result.should.equal(
        ["arn:aws:elasticloadbalancing:us-east-1:1:loadbalancer/my-lb/50dc6c495c0c9188"]
    )
