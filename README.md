# CostReduce

![Tests](https://github.com/CostReduce/cli/workflows/Tests/badge.svg?branch=master&event=push)
[![Requirements Status](https://requires.io/github/CostReduce/cli/requirements.svg?branch=master)](https://requires.io/github/CostReduce/cli/requirements/?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d638c6d95549442c97f2d6efb56f3de7)](https://www.codacy.com/gh/CostReduce/cli?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CostReduce/cli&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/d638c6d95549442c97f2d6efb56f3de7)](https://www.codacy.com/gh/CostReduce/cli?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CostReduce/cli&amp;utm_campaign=Badge_Coverage)
![GitHub](https://img.shields.io/github/license/costreduce/cli)

## Usage
### Install
For use this project, you need to install :
```
pip install costreduce
```
After install is complete. You can use the `costreduce --help` command.

### First Run
Check that you have correctly configured the [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
```
costreduce analyze --provider aws --service ec2 --region us-east-1
```
## Developement
### Requirements
Check that you have correctly configured the [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
For install requirements.
```
poetry install
```
For launch virtual env.
```
poetry shell
```
### Analyze cli
```
python costreduce/main.py analyze --provider aws --service ec2 --region us-east-1
```
