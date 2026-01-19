#!/usr/bin/env python3
from typing import Optional, Dict, Any

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class CloudWatchLogsGroup(AutomationTool):
    name = "cloudwatchlogs_log_group"
    module = "cloudwatchlogs_log_group"
    category = "aws_monitoring"
    description = "Manage AWS CloudWatch Logs log groups"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        log_group_name: str,
        state: str = "present",
        retention: Optional[int] = None,
        kms_key_id: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS CloudWatch Logs log group.

        Args:
            log_group_name: Name of the log group
            state: Whether the log group should be present or absent
            retention: Retention period in days
            kms_key_id: KMS key ID for encryption
            tags: Dictionary of tags to apply to the log group
            purge_tags: Remove tags not defined in module
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with log group details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "log_group_name": log_group_name,
            "state": state,
            "purge_tags": purge_tags,
        }
        
        # Add retention period
        if retention:
            module_args["retention"] = retention
        
        # Add KMS encryption
        if kms_key_id:
            module_args["kms_key_id"] = kms_key_id
        
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


def create_lambda_log_group(function_name: str, retention_days: int = 14):
    """Helper function to create log group for Lambda function.
    
    Args:
        function_name: Name of the Lambda function
        retention_days: Log retention period in days
    
    Returns:
        Dictionary of parameters for cloudwatchlogs_log_group
    """
    return {
        "log_group_name": f"/aws/lambda/{function_name}",
        "retention": retention_days
    }


def create_application_log_group(
    application_name: str,
    environment: str = "prod",
    retention_days: int = 30
):
    """Helper function to create application log group.
    
    Args:
        application_name: Name of the application
        environment: Environment (dev, staging, prod)
        retention_days: Log retention period in days
    
    Returns:
        Dictionary of parameters for cloudwatchlogs_log_group
    """
    return {
        "log_group_name": f"/aws/application/{application_name}/{environment}",
        "retention": retention_days
    }