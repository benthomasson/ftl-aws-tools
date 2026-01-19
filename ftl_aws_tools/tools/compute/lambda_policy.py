#!/usr/bin/env python3
from typing import Optional, Dict, Any

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class LambdaPolicy(AutomationTool):
    name = "lambda_policy"
    module = "lambda_policy"
    category = "aws_compute"
    description = "Manage AWS Lambda function policies and permissions"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        function_name: str,
        state: str = "present",
        alias: Optional[str] = None,
        version: Optional[int] = None,
        statement_id: Optional[str] = None,
        action: Optional[str] = None,
        principal: Optional[str] = None,
        source_arn: Optional[str] = None,
        source_account: Optional[str] = None,
        event_source_token: Optional[str] = None,
        qualifier: Optional[str] = None,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS Lambda function policy.

        Args:
            function_name: Name of the Lambda function
            state: Whether the policy should be present or absent
            alias: Function alias for the policy
            version: Function version for the policy
            statement_id: Unique statement ID for the policy
            action: AWS Lambda action to allow (e.g., lambda:InvokeFunction)
            principal: Principal to grant permission to
            source_arn: ARN of the source service
            source_account: Account ID of the source service
            event_source_token: Token for event source validation
            qualifier: Function qualifier (version or alias)
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with policy details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "function_name": function_name,
            "state": state,
        }
        
        # Add alias or version
        if alias:
            module_args["alias"] = alias
        elif version:
            module_args["version"] = version
        
        # Add permission details
        if statement_id:
            module_args["statement_id"] = statement_id
        if action:
            module_args["action"] = action
        if principal:
            module_args["principal"] = principal
        if source_arn:
            module_args["source_arn"] = source_arn
        if source_account:
            module_args["source_account"] = source_account
        if event_source_token:
            module_args["event_source_token"] = event_source_token
        if qualifier:
            module_args["qualifier"] = qualifier
        
        # Add region
        if region:
            module_args["region"] = region
        
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output


def create_api_gateway_permission(
    function_name: str,
    statement_id: str,
    api_gateway_arn: str,
    source_account: Optional[str] = None
):
    """Helper function to create API Gateway invoke permission.
    
    Args:
        function_name: Name of the Lambda function
        statement_id: Unique statement ID
        api_gateway_arn: ARN of the API Gateway
        source_account: Account ID for additional security
    
    Returns:
        Dictionary of parameters for lambda_policy
    """
    params = {
        "function_name": function_name,
        "statement_id": statement_id,
        "action": "lambda:InvokeFunction",
        "principal": "apigateway.amazonaws.com",
        "source_arn": api_gateway_arn
    }
    
    if source_account:
        params["source_account"] = source_account
    
    return params


def create_alb_permission(
    function_name: str,
    statement_id: str,
    load_balancer_arn: str,
    source_account: Optional[str] = None
):
    """Helper function to create Application Load Balancer invoke permission.
    
    Args:
        function_name: Name of the Lambda function
        statement_id: Unique statement ID
        load_balancer_arn: ARN of the Application Load Balancer
        source_account: Account ID for additional security
    
    Returns:
        Dictionary of parameters for lambda_policy
    """
    params = {
        "function_name": function_name,
        "statement_id": statement_id,
        "action": "lambda:InvokeFunction",
        "principal": "elasticloadbalancing.amazonaws.com",
        "source_arn": load_balancer_arn
    }
    
    if source_account:
        params["source_account"] = source_account
    
    return params


def create_s3_permission(
    function_name: str,
    statement_id: str,
    bucket_arn: str,
    source_account: Optional[str] = None
):
    """Helper function to create S3 bucket notification permission.
    
    Args:
        function_name: Name of the Lambda function
        statement_id: Unique statement ID
        bucket_arn: ARN of the S3 bucket
        source_account: Account ID for additional security
    
    Returns:
        Dictionary of parameters for lambda_policy
    """
    params = {
        "function_name": function_name,
        "statement_id": statement_id,
        "action": "lambda:InvokeFunction",
        "principal": "s3.amazonaws.com",
        "source_arn": bucket_arn
    }
    
    if source_account:
        params["source_account"] = source_account
    
    return params