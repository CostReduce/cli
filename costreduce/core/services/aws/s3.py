# -*- coding: utf-8 -*-
import logging
import botocore
import sys
from costreduce.core.providers.aws import account_id

logger = logging.getLogger(__name__)


class S3Analyze:  # pragma: no cover
    def __init__(self, sdk, region):
        self.sdk = sdk
        self.region = region
        self.s3 = S3(self.sdk, self.region)

    def analyze(self):
        analyze = list()
        # analyze.append(self.s3.bucket_without_lifecycle())
        analyze.append(self.s3.bucket_default_storage_class())
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

    def bucket_default_storage_class(self):
        response = list()
        buckets_names = self._get_all_bucket()
        for bucket in buckets_names:
            storage_class = self._get_bucket_storage_class(bucket)
            total_object = len(storage_class)
            count_storage_class = self._count_standard_storage_class(storage_class)

            if count_storage_class == total_object:
                data = "All object in bucket s3 use default Storage Class : " + bucket
                logger.debug(data)
                response.append(data)
            elif total_object <= (count_storage_class / 2):
                data = "Half of the s3 object use default Storage Class : " + bucket
                logger.debug(data)
                response.append(data)
        return response

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

    def _get_bucket_storage_class(self, bucket):
        response = list()
        try:
            s3_bucket_object = self.client_s3.list_objects_v2(Bucket=bucket)["Contents"]
            for object in s3_bucket_object:
                response.append(object["StorageClass"])
        except botocore.exceptions.ClientError as error:
            return ""
        return response

    def _count_standard_storage_class(self, storage_class):
        response = 0
        for storage in storage_class:
            if storage in "STANDARD":
                response += 1
        return response
