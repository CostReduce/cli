# -*- coding: utf-8 -*-
import logging
from src.core.providers.aws import account_id

logger = logging.getLogger(__name__)


class Ec2Analyze:
    """ Class for Analyze all EC2 Services """

    def __init__(self, sts, region):
        """
        init function
        Arguments:
            sts: import boto3 globaly
            region: Cloud Provider region
        """
        self.sts = sts
        self.region = region
        self.compute_optimizer = ComputeOptimizer(self.sts, self.region)
        self.application_load_balancer = ApplicationLoadBalancer(self.sts, self.region)
        self.ec2 = Ec2(self.sts, self.region)

    def analyze(self):
        """
        Function for Analyze all services.
        Returns:
            Table for all check
        """
        analyze = list()
        # Compute Optimizer
        logger.info("Check Compute Optimizer")
        if self.compute_optimizer.is_active():
            analyze.append(self.compute_optimizer.ec2_recommendation())
        # EIP
        logger.info("Check for EIP")
        analyze.append(self.ec2.eip_is_not_attached())
        # ALB
        logger.info("Check for ALB")
        analyze.append(self.application_load_balancer.alb_listener_one_rule())

        logger.debug("Result of analyze : " + str(analyze))
        return analyze


class Ec2:
    """ Class for all EC2 services """

    def __init__(self, sts, region):
        """
        init function
        Arguments:
            sts: import boto3 globaly
            region: Cloud Provider region
        """
        self.sts = sts
        self.region = region
        self.client_ec2 = sts.client("ec2", region_name=region)

    def eip_is_not_attached(self):
        addresses_dict = self.client_ec2.describe_addresses()
        response = list()
        for eip_dict in addresses_dict["Addresses"]:
            if "InstanceId" not in eip_dict:
                data = "Remove EIPs when not in use : " + str(eip_dict["AllocationId"])
                logger.debug(data)
                response.append(data)
        return response


class ApplicationLoadBalancer:
    """ Class for all ALBv2 services """

    def __init__(self, sts, region):
        """
        init function
        Arguments:
            sts: import boto3 globaly
            region: Cloud Provider region
        """
        self.sts = sts
        self.region = region
        self.client = sts.client("elbv2", region_name=region)

    def alb_listener_one_rule(self):
        response = list()
        alb_listener_arn = self.__alb_listener_arn()
        for listenerArn in alb_listener_arn:
            rules_dict = self.client.describe_rules(ListenerArn=listenerArn)
            for rule in rules_dict["Rules"]:
                count = 0
                for i in rule["Conditions"]:
                    if rule["Priority"] != "default":
                        # print(rule)
                        count += 1
                if count < 2:
                    listener_to_elb = self.client.describe_listeners(
                        ListenerArns=[listenerArn]
                    )
                    elb_arn = listener_to_elb["Listeners"][0]["LoadBalancerArn"]
                    data = (
                        "Fusion this ALB "
                        + str(elb_arn)
                        + " because one ALB for one rules is so expensive."
                    )
                    if data not in response:
                        logger.debug(data)
                        response.append(data)
        return response

    def __alb_listener_arn(self):
        response = list()
        alb_arn = self.get_elb_arn()
        for alb in alb_arn:
            listeners_dict = self.client.describe_listeners(LoadBalancerArn=alb)
            for listener in listeners_dict["Listeners"]:
                response.append(listener["ListenerArn"])
        return response

    def get_elb_arn(self):
        alb_dict = self.client.describe_load_balancers()
        response = list()
        for alb in alb_dict["LoadBalancers"]:
            response.append(alb["LoadBalancerArn"])
        return response


class ComputeOptimizer:
    def __init__(self, sts, region):
        """
        init function
        Arguments:
            sts: import boto3 globaly
            region: Cloud Provider region
        """
        self.region = region
        self.client = sts.client("compute-optimizer", region_name=region)
        self.account_id = account_id()

    def is_active(self):
        """Check Compute Optimizer is active"""
        response = self.client.get_enrollment_status()
        if response["status"] != "Active":
            logger.error("Compute Optimizer enrollment status is " + response["status"])
            return False
        else:
            return True

    def ec2_recommendation(self):
        response = list()
        get_ec2_recommendation = self.client.get_ec2_instance_recommendations()
        for ec2_recommendation in get_ec2_recommendation["instanceRecommendations"]:
            if (
                ec2_recommendation["currentInstanceType"]
                != ec2_recommendation["recommendationOptions"][0]["instanceType"]
            ):
                ec2_instances_name = ec2_recommendation["instanceName"]
                ec2_instances_current_instance_type = ec2_recommendation[
                    "currentInstanceType"
                ]
                ec2_instances_recommendation_instance_type = ec2_recommendation[
                    "recommendationOptions"
                ][0]["instanceType"]
                data = (
                    "For instance "
                    + ec2_instances_name
                    + " change type "
                    + ec2_instances_current_instance_type
                    + " to "
                    + ec2_instances_recommendation_instance_type
                )
                if data not in response:
                    logger.debug(data)
                    response.append(data)
        return response
