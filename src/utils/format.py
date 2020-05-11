# -*- coding: utf-8 -*-
from texttable import Texttable
import logging

logger = logging.getLogger(__name__)


def grid(data, service, provider):
    count = 0
    table = Texttable()
    table.set_cols_width([5, 10, 10, 200])
    table.add_rows([["#", "Provider", "Service", "Description"]])
    for toto in data:
        for i in toto:
            table.add_row([count, provider, service, i])
            count += 1
    response = table.draw()
    logger.info(response)
    return response
