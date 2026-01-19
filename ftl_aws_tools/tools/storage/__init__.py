"""AWS Storage Service Tools.

This module contains automation tools for AWS storage services:

- S3 buckets and object management
- EBS volumes and snapshots
- EFS file systems
- Storage gateways

Available tools:
    - s3_bucket: Manage S3 buckets
    - s3_object: Manage S3 objects
    - ebs_volume: Manage EBS volumes
    - efs_filesystem: Manage EFS file systems

Usage:
    with automation(tool_packages=["ftl_aws_tools.tools.storage"]) as ftl:
        ftl.s3_bucket(name="my-bucket", state="present")
        ftl.s3_object(bucket="my-bucket", key="file.txt", src="local-file.txt")
"""

# Tool imports
from .s3_bucket import S3Bucket

__all__ = [
    'S3Bucket'
]