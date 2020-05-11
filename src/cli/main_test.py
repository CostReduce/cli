# -*- coding: utf-8 -*-
from click.testing import CliRunner
from src.cli.main import analyze
from src.cli.main import report


def test_analyze():
    runner = CliRunner()
    result = runner.invoke(analyze, ["--service", "ec2", "--provider", "aws"])
    assert result.exit_code == 0
    assert result.output == "Launch analyze for ec2 on aws!\n"


def test_report():
    runner = CliRunner()
    result = runner.invoke(report, ["--service", "ec2", "--provider", "aws"])
    assert result.exit_code == 0
    assert result.output == "Launch report for ec2 on aws!\n"
