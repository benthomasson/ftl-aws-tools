#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class IAMRole(AutomationTool):
    name = "iam_role"
    module = "iam_role"
    category = "aws_security"
    description = "Manage AWS IAM roles"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name: str,
        state: str = "present",
        assume_role_policy_document: Optional[Dict[str, Any]] = None,
        managed_policies: Optional[List[str]] = None,
        max_session_duration: Optional[int] = None,
        path: str = "/",
        description: Optional[str] = None,
        permissions_boundary: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        purge_policies: bool = True,
        create_instance_profile: bool = True,
        delete_instance_profile: bool = False,
        wait: bool = True,
        wait_timeout: int = 120,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS IAM role.

        Args:
            name: Name of the IAM role
            state: Whether the role should be present or absent
            assume_role_policy_document: Trust policy document
            managed_policies: List of managed policy ARNs
            max_session_duration: Maximum session duration in seconds
            path: IAM path for the role
            description: Description of the role
            permissions_boundary: Permissions boundary policy ARN
            tags: Dictionary of tags to apply to the role
            purge_tags: Remove tags not defined in module
            purge_policies: Remove policies not defined in module
            create_instance_profile: Create EC2 instance profile
            delete_instance_profile: Delete instance profile when deleting role
            wait: Wait for role to be created
            wait_timeout: Timeout for wait operation
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with role details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "name": name,
            "state": state,
            "path": path,
            "purge_tags": purge_tags,
            "purge_policies": purge_policies,
            "create_instance_profile": create_instance_profile,
            "delete_instance_profile": delete_instance_profile,
            "wait": wait,
            "wait_timeout": wait_timeout,
        }
        
        # Add trust policy
        if assume_role_policy_document:
            module_args["assume_role_policy_document"] = assume_role_policy_document
        
        # Add managed policies
        if managed_policies:
            module_args["managed_policies"] = managed_policies
        
        # Add session duration
        if max_session_duration:
            module_args["max_session_duration"] = max_session_duration
        
        # Add description
        if description:
            module_args["description"] = description
        
        # Add permissions boundary
        if permissions_boundary:
            module_args["permissions_boundary"] = permissions_boundary
        
        # Add tags
        if tags:
            module_args["tags"] = tags
        
        # Add region
        if region:
            module_args["region"] = region
        
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output


def create_service_trust_policy(services: List[str]):
    """Helper function to create a service trust policy.
    
    Args:
        services: List of AWS service principals (e.g., lambda.amazonaws.com)
    
    Returns:
        Trust policy document dictionary
    """
    principals = [f"{service}" for service in services]
    
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": principals
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }


def create_cross_account_trust_policy(account_ids: List[str], external_id: Optional[str] = None):
    """Helper function to create a cross-account trust policy.
    
    Args:
        account_ids: List of AWS account IDs
        external_id: External ID for additional security
    
    Returns:
        Trust policy document dictionary
    """
    principals = [f"arn:aws:iam::{account_id}:root" for account_id in account_ids]
    
    statement = {
        "Effect": "Allow",
        "Principal": {
            "AWS": principals
        },
        "Action": "sts:AssumeRole"
    }
    
    if external_id:
        statement["Condition"] = {
            "StringEquals": {
                "sts:ExternalId": external_id
            }
        }
    
    return {
        "Version": "2012-10-17",
        "Statement": [statement]
    }


def create_lambda_execution_role():
    """Helper function to create Lambda execution role trust policy.
    
    Returns:
        Trust policy document for Lambda execution
    """
    return create_service_trust_policy(["lambda.amazonaws.com"])