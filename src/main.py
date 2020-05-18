# -*- coding: utf-8 -*-
import logging
import click
import click_log
import sys
from src.core.analyze import Analyze
from src.utils.format import grid

logger = logging.getLogger()
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
click_log.basic_config(logger)
logger.setLevel(logging.INFO)
click_log.ColorFormatter.colors["info"] = dict(fg="green")
click_log.ColorFormatter.colors["warning"] = dict(fg="yellow")
click_log.ColorFormatter.colors["error"] = dict(fg="red")


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--provider",
    prompt="Cloud Provider",
    default="aws",
    help="Get your Cloud Provider.",
)
@click.option(
    "--service", prompt="Service name", default="ec2", help="Get Service Name."
)
@click.option(
    "--region", prompt="Provider region", default="us-east-1", help="Get Region Name."
)
def analyze(provider, service, region):
    logger.info("Launch analyze for %s on %s ..." % (service, provider))
    result = Analyze(provider, service, region)
    if provider == "aws":
        response = result.aws()
    else:
        logger.info(str(provider) + " don't allow!")
        sys.exit(1)

    grid(response, provider, service, region)


if __name__ == "__main__":
    cli()
