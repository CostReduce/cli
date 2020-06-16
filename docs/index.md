# Welcome to CostReduce Docs

## Install

Check that you have correctly configured the [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
To install CostReduce, simply use the following command.
````
pip install -U costreduce
````

## Usage

Once the click is installed, you can start your first analysis of your AWS account.

````
costreduce analyze --provider aws --service ec2 --region us-east-1
````

## Supported service
| Provider      |     Service     |  Description  |
| ------------- |: -------------: | : --------- : |
| AWS           |        ec2      | ALB, ComputeOptimizer, EIP, EBS |
| AWS           |   cloudwatch    | Logs |