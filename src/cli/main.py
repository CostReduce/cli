# -*- coding: utf-8 -*-
"""
main.py
====================================
This is entrypoint
"""

import click
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--provider", prompt="Cloud Provider", help="Get your Cloud Provider.")
@click.option("--service", prompt="Service name", help="Get Service Name.")
def analyze(provider, service):
    """
    Return analyze for service on provider.
    Parameters
    ----------
    provider : str
        A string indicating the provider name.
    service : str
        A string indicating the service name.
    """
    click.echo("Launch analyze for %s on %s!" % (service, provider))


@cli.command()
@click.option("--provider", prompt="Cloud Provider", help="Get your Cloud Provider.")
@click.option("--service", prompt="Service name", help="Get Service Name.")
def report(provider, service):
    """
    Return report for service on provider.
    Parameters
    ----------
    provider : str
        A string indicating the provider name.
    service : str
        A string indicating the service name.
    """
    click.echo("Launch report for %s on %s!" % (service, provider))


if __name__ == "__main__":
    cli()
