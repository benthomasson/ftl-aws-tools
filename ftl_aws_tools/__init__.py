"""FTL AWS Tools - AWS automation tools for FTL Automation framework.

This package provides AWS-specific automation tools built on the FTL Automation
framework. Tools are organized by AWS service categories for easy discovery
and logical grouping.

Usage:
    from ftl_automation import automation
    
    with automation(
        tool_packages=["ftl_aws_tools.tools.compute"],
        tools=["ec2_instance", "ec2_security_group"]
    ) as ftl:
        ftl.ec2_instance(name="my-instance", image_id="ami-12345")

Available tool categories:
    - compute: EC2, Lambda, Auto Scaling
    - storage: S3, EBS, EFS
    - networking: VPC, Subnets, Route Tables
    - database: RDS, DynamoDB
    - security: IAM, Security Groups
    - monitoring: CloudWatch, CloudTrail
"""

__version__ = "0.1.0"
__author__ = "FTL Automation"

# Re-export commonly used classes and functions for convenience
from .utils import AWSConfig, get_aws_region, get_aws_account_id

__all__ = [
    "__version__",
    "__author__",
    "AWSConfig",
    "get_aws_region", 
    "get_aws_account_id",
]