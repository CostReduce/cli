# -*- coding: utf-8 -*-
from texttable import Texttable
import logging

logger = logging.getLogger(__name__)


def grid(desc, provider, type, service, region):
    """
    Create and print grid for result

    Arguments:
        desc: Description of actions to reduce costs
        provider: Cloud Provider (aws)
        type: Type (Compute,Storage)
        service: Cloud Service (ec2,cloudwatch)
        region: Cloud Provider region
    Returns:
        print grid
    """
    count = 0
    table = Texttable()
    table.set_cols_width([5, 10, 10, 10, 10, 180])
    table.add_rows([["#", "Provider", "Type", "Region", "Service", "Description"]])
    for toto in desc:
        for i in toto:
            table.add_row([count, provider, type, region, service, i])
            count += 1
    response = table.draw()
    logger.info(response)
    return response
