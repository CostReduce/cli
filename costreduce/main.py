# -*- coding: utf-8 -*-
import logging
import click
import click_log
import sys
from costreduce.core.analyze import Analyze
from costreduce.utils.format import grid

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
    "-p",
    "--provider",
    prompt="Cloud Provider",
    default="aws",
    help="Get your Cloud Provider.",
    type=click.Choice(["aws"], case_sensitive=False),
)
@click.option(
    "-s",
    "--service",
    prompt="Service name",
    default="ec2",
    help="Get Service Name.",
    type=click.Choice(["ec2", "cloudwatch", "s3"], case_sensitive=False),
)
@click.option(
    "-r",
    "--region",
    prompt="Provider region",
    default="us-east-1",
    help="Get Region Name.",
)
def analyze(provider, service, region):
    logger.info("Launch analyze for %s on %s ..." % (service, provider))
    result = Analyze(provider, service, region)
    if provider == "aws":
        response = result.aws()
    else:
        logger.info("Provider " + str(provider) + " don't allow!")
        sys.exit(1)

    if service == "s3":
        type = "Storage"
    elif service == "ec2":
        type = "Compute"
    elif service == "cloudwatch":
        type = "Management"
    else:
        type = "null"

    grid(response, provider, type, service, region)


if __name__ == "__main__":
    cli()
