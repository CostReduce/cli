# -*- coding: utf-8 -*-
import logging
import sys
import click
import click_log
import boto3
from src.core.services.aws.ec2 import Ec2
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
    if provider == "aws":
        if service == "ec2":
            ec2 = Ec2(boto3, region).analyze()
            grid(ec2, service, provider)
        else:
            logger.info(str(service) + " don't allow!")
            sys.exit(1)
    else:
        logger.info(str(provider) + " don't allow!")
        sys.exit(1)


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
def report(provider, service, region):
    click.echo("Launch report for %s on %s!" % (service, provider))


if __name__ == "__main__":
    cli()
