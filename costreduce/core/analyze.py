# -*- coding: utf-8 -*-
import logging
import sys
import boto3
from costreduce.core.services.aws.ec2 import Ec2Analyze
from costreduce.core.services.aws.cloudwatch import CloudwatchAnalyze
from costreduce.core.services.aws.s3 import S3Analyze


logger = logging.getLogger(__name__)


class Analyze:
    """ Entrypoint for Analyze command """

    def __init__(self, provider, service, region, sdk=boto3):
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
        self.sdk = sdk

    def aws(self):
        """
        Entrypoint for AWS provider
        """
        if self.service == "ec2":
            return Ec2Analyze(self.sdk, self.region).analyze()
        elif self.service == "s3":
            return S3Analyze(self.sdk, self.region).analyze()
        elif self.service == "cloudwatch":
            return CloudwatchAnalyze(self.sdk, self.region).analyze()
        else:
            logger.info("Service " + str(self.service) + " don't allow!")
            sys.exit(1)
