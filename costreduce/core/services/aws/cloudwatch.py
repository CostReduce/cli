# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class CloudwatchAnalyze:
    """ Class for Analyze all EC2 Services """

    def __init__(self, sdk, region):
        """
        init function
        Arguments:
            sdk: import boto3 globaly
            region: Cloud Provider region
        """
        self.sdk = sdk
        self.region = region
        self.cloudwatch = Cloudwatch(self.sdk, self.region)

    def analyze(self):
        """
        Function for Analyze all services.
        Returns:
            Table for all check
        """
        analyze = list()

        logger.info("Check for CloudWatch Logs")
        analyze.append(self.cloudwatch.get_log_groups())

        logger.debug("Result of analyze : " + str(analyze))
        return analyze


class Cloudwatch:
    """ Class for all CloudWatch services"""

    def __init__(self, sdk, region):
        """
        init function
        Arguments:
            sdk: import boto3 globaly
            region: Cloud Provider region
        """
        self.region = region
        self.client_logs = sdk.client("logs", region_name=region)

    def _list_log_groups(self, next_token=None):
        opts = {"limit": 50}
        if next_token:
            opts["nextToken"] = next_token
        log_groups_response = self.client_logs.describe_log_groups(**opts)
        if log_groups_response:
            for log_group in log_groups_response["logGroups"]:
                yield log_group
            if "nextToken" in log_groups_response:
                yield from self._list_log_groups(log_groups_response["nextToken"])

    def get_log_groups(self):
        response = list()
        for log_group in self._list_log_groups():
            if "retentionInDays" not in log_group:
                log_group_name = log_group["logGroupName"]
                data = (
                    "Add retention in "
                    + str(log_group_name)
                    + " because currently you store the data without an end date."
                )
                if data not in response:
                    logger.debug(data)
                    response.append(data)
            return response
