# -*- coding: utf-8 -*-
from src.core.providers.aws import account_id
from moto import mock_sts


@mock_sts
def test_account_id(aws_credentials):
    account_id().should.equal("123456789012")
