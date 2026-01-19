"""AWS Compute Service Tools.

This module contains automation tools for AWS compute services:

- EC2 instances and instance management
- Lambda functions 
- Auto Scaling groups
- Key pairs and security groups
- AMI management

Available tools:
    - ec2_instance: Manage EC2 instances
    - ec2_security_group: Manage EC2 security groups  
    - ec2_key: Manage EC2 key pairs
    - ec2_ami: Manage AMIs
    - lambda_function: Manage Lambda functions

Usage:
    with automation(tool_packages=["ftl_aws_tools.tools.compute"]) as ftl:
        ftl.ec2_instance(
            name="web-server",
            image_id="ami-12345", 
            instance_type="t3.micro"
        )
"""

# Tool imports
from .lambda_function import LambdaFunction
from .lambda_policy import LambdaPolicy

__all__ = [
    'LambdaFunction',
    'LambdaPolicy'
]