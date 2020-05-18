# -*- coding: utf-8 -*-
import logging
import boto3

# import sys
# from src.core.services.aws.ec2 import Ec2
# from src.utils.format import grid

logger = logging.getLogger(__name__)


def account_id():
    response = boto3.client("sts").get_caller_identity().get("Account")
    logger.info("Account ID: " + response)
    return response


#
# class AwsAnalyze:
#     def __init__(self, service, region):
#         self.provider = "aws"
#         self.service = service
#         self.region = region
#
#     def get(self):
#         if self.service == "ec2":
#             ec2 = Ec2(boto3, self.region).analyze()
#             grid(ec2, self.service, self.provider)
#         else:
#             logger.info(str(self.service) + " don't allow!")
#             sys.exit(1)
