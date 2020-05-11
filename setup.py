# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

# from package import Package

setup(
    name="CostReduce",
    description='An essential toolset that eases server administration',
    version="0.0.1",
    author="Maxence Maireaux",
    author_email="maxence@maireaux.fr",
    url="https://www.costreduce.io",
    license="MIT",
    python_requires=">=3.6,<4.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points="""
          [console_scripts]
          costreduce = src.cli.main:cli
      """,
)
