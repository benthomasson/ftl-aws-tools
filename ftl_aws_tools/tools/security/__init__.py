"""AWS Security Service Tools.

This module contains automation tools for AWS security services:

- IAM users, roles, and policies
- Security groups and NACLs
- KMS keys and encryption
- AWS Secrets Manager

Available tools:
    - iam_role: Manage IAM roles
    - iam_policy: Manage IAM policies
    - iam_user: Manage IAM users
    - security_group: Manage security groups
    - kms_key: Manage KMS keys

Usage:
    with automation(tool_packages=["ftl_aws_tools.tools.security"]) as ftl:
        ftl.iam_role(
            name="MyRole",
            assume_role_policy_document=policy_doc,
            state="present"
        )
"""

# Tool imports will be added here as tools are implemented
# from .iam_role import IAMRole
# from .iam_policy import IAMPolicy
# from .security_group import SecurityGroup

__all__ = [
    # Tool classes will be listed here
]