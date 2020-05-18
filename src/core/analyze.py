# -*- coding: utf-8 -*-
import logging
import sys
import boto3
from src.core.services.aws.ec2 import Ec2


logger = logging.getLogger(__name__)


class Analyze:
    def __init__(self, provider, service, region):
        self.provider = provider
        self.service = service
        self.region = region

    def aws(self):
        if self.service == "ec2":
            return Ec2(boto3, self.region).analyze()
        else:
            logger.info(str(self.service) + " don't allow!")
            sys.exit(1)
