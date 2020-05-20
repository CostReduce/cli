# -*- coding: utf-8 -*-
import logging
import sys
import boto3
from src.core.services.aws.ec2 import Ec2Analyze
from src.core.services.aws.cloudwatch import CloudwatchAnalyze


logger = logging.getLogger(__name__)


class Analyze:
    """ Entrypoint for Analyze command """

    def __init__(self, provider, service, region):
        """
        init function
        Arguments:
            provider: Cloud Provider (aws)
            service: Cloud Service (ec2,cloudwatch)
            region: Cloud Provider region
        """
        self.provider = provider
        self.service = service
        self.region = region

    def aws(self):
        """
        Entrypoint for AWS provider
        """
        if self.service == "ec2":
            return Ec2Analyze(boto3, self.region).analyze()
        elif self.service == "cloudwatch":
            return CloudwatchAnalyze(boto3, self.region).analyze()
        else:
            logger.info("Service " + str(self.service) + " don't allow!")
            sys.exit(1)
