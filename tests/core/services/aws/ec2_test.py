# -*- coding: utf-8 -*-
import boto3
import pytest
from moto import mock_elbv2, mock_ec2, mock_sts
from costreduce.core.services.aws.ec2 import ApplicationLoadBalancer, Ec2, Ec2Analyze


@pytest.fixture()
def fixture_alb(boto3_mock):
    mock_ec2().start()
    mock_elbv2().start()
    conn = boto3_mock.client("elbv2", region_name="us-east-1")
    ec2 = boto3_mock.resource("ec2", region_name="us-east-1")

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

    response = conn.create_load_balancer(
        Name="my-lb",
        Subnets=[subnet1.id, subnet2.id],
        SecurityGroups=[security_group.id],
        Scheme="internal",
        Tags=[{"Key": "key_name", "Value": "a_value"}],
    )

    load_balancer_arn = response.get("LoadBalancers")[0].get("LoadBalancerArn")

    response = conn.create_target_group(
        Name="a-target",
        Protocol="HTTP",
        Port=8080,
        VpcId=vpc.id,
        HealthCheckProtocol="HTTP",
        HealthCheckPort="8080",
        HealthCheckPath="/",
        HealthCheckIntervalSeconds=5,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,
        UnhealthyThresholdCount=2,
        Matcher={"HttpCode": "200"},
    )
    target_group = response.get("TargetGroups")[0]

    # Plain HTTP listener
    response = conn.create_listener(
        LoadBalancerArn=load_balancer_arn,
        Protocol="HTTP",
        Port=80,
        DefaultActions=[
            {"Type": "forward", "TargetGroupArn": target_group.get("TargetGroupArn")}
        ],
    )
    listener = response.get("Listeners")[0]
    http_listener_arn = listener.get("ListenerArn")
    yield { "load_balancer_arn": load_balancer_arn, "http_listener_arn": http_listener_arn }
    mock_elbv2().stop()
    mock_ec2().stop()


@mock_elbv2
def test_get_alb_arn_is_empty(boto3_mock):
    aws = ApplicationLoadBalancer(boto3_mock, "us-east-1")
    result = aws.get_elb_arn()
    result.should.equal([])


def test_get_alb_arn_is_not_empty(boto3_mock, fixture_alb):
    aws = ApplicationLoadBalancer(boto3_mock, "us-east-1")
    result = aws.get_elb_arn()
    result.should.equal(
        [fixture_alb["load_balancer_arn"]]
    )


@mock_ec2
@mock_elbv2
def test_get_alb_listener_arn_is_empty(boto3_mock):
    aws = ApplicationLoadBalancer(boto3_mock, "us-east-1")
    result = aws.get_alb_listener_arn()
    result.should.equal([])


def test_get_alb_listener_arn_is_not_empty(boto3_mock, fixture_alb):
    aws = ApplicationLoadBalancer(boto3_mock, "us-east-1")
    result = aws.get_alb_listener_arn()
    result.should.equal([fixture_alb["http_listener_arn"]])


@mock_ec2
@mock_elbv2
def test_get_alb_listener_one_rule_is_empty(boto3_mock):
    aws = ApplicationLoadBalancer(boto3_mock, "us-east-1")
    result = aws.alb_listener_one_rule()
    result.should.equal([])


def test_get_alb_listener_one_rule_is_not_empty(boto3_mock, fixture_alb):
    aws = ApplicationLoadBalancer(boto3_mock, "us-east-1")
    result = aws.alb_listener_one_rule()
    print(result)
    result.should.equal(
        [
            "Fusion this ALB "
            + fixture_alb["load_balancer_arn"]
            + " because one ALB for one rules is so expensive."
        ]
    )


@mock_ec2
def test_ebs_is_not_attached_empty(boto3_mock):
    aws = Ec2(boto3_mock, "us-east-1")
    result = aws.ebs_is_not_attached()
    result.should.equal([])


@mock_ec2
def test_ebs_is_not_attached_not_empty(boto3_mock):
    conn = boto3.client("ec2", region_name="us-east-1")
    conn.create_volume(Size=80, AvailabilityZone="us-east-1a")
    all_volumes = conn.describe_volumes()
    current_volume = all_volumes["Volumes"][0]["VolumeId"]

    aws = Ec2(boto3_mock, "us-east-1")
    result = aws.ebs_is_not_attached()
    result.should.equal(["Remove this EBS " + current_volume + " because is not use."])


@mock_ec2
def test_eip_is_not_attached_empty(boto3_mock):
    aws = Ec2(boto3_mock, "us-east-1")
    result = aws.eip_is_not_attached()
    result.should.equal([])
