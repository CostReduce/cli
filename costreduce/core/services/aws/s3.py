# -*- coding: utf-8 -*-
import logging
import botocore
from costreduce.core.providers.aws import account_id

logger = logging.getLogger(__name__)


class S3Analyze:  # pragma: no cover
    def __init__(self, sdk, region):
        self.sdk = sdk
        self.region = region
        self.s3 = S3(self.sdk, self.region)

    def analyze(self):
        analyze = list()
        analyze.append(self.s3.bucket_without_lifecycle())
        return analyze


class S3:
    def __init__(self, sdk, region):
        """
        init function
        Arguments:
            sdk: import boto3 globaly
            region: Cloud Provider region
        """
        self.sdk = sdk
        self.region = region
        self.client_s3 = sdk.client("s3", region_name=region)

    def bucket_without_lifecycle(self):
        response = list()
        buckets_names = self._get_all_bucket()
        for bucket in buckets_names:
            lifecycle = self._get_bucket_lifecycle(bucket)
            if "Rules" not in lifecycle:
                data = "Bucket s3 without LifeCycle Configuration : " + bucket
                logger.debug(data)
                response.append(data)
        return response

    def _get_all_bucket(self):
        s3_dict = self.client_s3.list_buckets()
        buckets = list()
        for bucket in s3_dict["Buckets"]:
            bucket_name = bucket["Name"]
            buckets.append(bucket_name)
        return buckets

    def _get_bucket_lifecycle(self, bucket):
        try:
            s3_bucket_lifecycle = self.client_s3.get_bucket_lifecycle_configuration(
                Bucket=bucket
            )
        except botocore.exceptions.ClientError as error:
            return ""
        return s3_bucket_lifecycle
