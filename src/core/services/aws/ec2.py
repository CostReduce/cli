# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class Ec2:
    def __init__(self, sts, region):
        self.region = region
        self.client_ec2 = sts.client("ec2", region_name=region)
        self.client_elbv2 = sts.client("elbv2", region_name=region)

    def analyze(self):
        analyze = list()
        # EIP
        logger.info("Check for EIP")
        analyze.append(self._free_eip())
        # ALB
        logger.info("Check for ALB")
        analyze.append(self._alb_listener_one_rule())

        logger.debug("Result of analyze : " + str(analyze))
        return analyze

    def _free_eip(self):
        addresses_dict = self.client_ec2.describe_addresses()
        response = list()
        for eip_dict in addresses_dict["Addresses"]:
            if "InstanceId" not in eip_dict:
                data = "Remove EIPs when not in use : " + str(eip_dict["AllocationId"])
                logger.debug(data)
                response.append(data)
        return response

    def _alb_listener_one_rule(self):
        response = list()
        alb_listener_arn = self.__alb_listener_arn()
        for listenerArn in alb_listener_arn:
            rules_dict = self.client_elbv2.describe_rules(ListenerArn=listenerArn)
            for rule in rules_dict["Rules"]:
                count = 0
                for i in rule["Conditions"]:
                    if rule["Priority"] != "default":
                        # print(rule)
                        count += 1
                if count < 2:
                    listener_to_elb = self.client_elbv2.describe_listeners(
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
            listeners_dict = self.client_elbv2.describe_listeners(LoadBalancerArn=alb)
            for listener in listeners_dict["Listeners"]:
                response.append(listener["ListenerArn"])
        return response

    def get_elb_arn(self):
        alb_dict = self.client_elbv2.describe_load_balancers()
        response = list()
        for alb in alb_dict["LoadBalancers"]:
            response.append(alb["LoadBalancerArn"])
        return response
