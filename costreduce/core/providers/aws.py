# -*- coding: utf-8 -*-
import logging
import boto3

logger = logging.getLogger(__name__)


def account_id():
    """ Get current account id """
    response = boto3.client("sts").get_caller_identity().get("Account")
    logger.debug("Account ID: " + response)
    return response
