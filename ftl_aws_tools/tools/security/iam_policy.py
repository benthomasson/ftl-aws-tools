#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class IAMPolicy(AutomationTool):
    name = "iam_policy"
    module = "iam_policy"
    category = "aws_security"
    description = "Manage AWS IAM managed policies"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name: str,
        state: str = "present",
        policy: Optional[Dict[str, Any]] = None,
        path: str = "/",
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        only_version: bool = False,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS IAM managed policy.

        Args:
            name: Name of the IAM policy
            state: Whether the policy should be present or absent
            policy: Policy document as a dictionary
            path: IAM path for the policy
            description: Description of the policy
            tags: Dictionary of tags to apply to the policy
            purge_tags: Remove tags not defined in module
            only_version: Only create new version if policy exists
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with policy details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "name": name,
            "state": state,
            "path": path,
            "purge_tags": purge_tags,
            "only_version": only_version,
        }
        
        # Add policy document
        if policy:
            module_args["policy"] = policy
        
        # Add description
        if description:
            module_args["description"] = description
        
        # Add tags
        if tags:
            module_args["tags"] = tags
        
        # Add region
        if region:
            module_args["region"] = region
        
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module_locally(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output


def create_policy_statement(
    effect: str,
    actions: List[str],
    resources: List[str],
    conditions: Optional[Dict[str, Any]] = None,
    principals: Optional[Dict[str, Any]] = None
):
    """Helper function to create a policy statement.
    
    Args:
        effect: Allow or Deny
        actions: List of IAM actions
        resources: List of resource ARNs
        conditions: Condition block
        principals: Principal specification (for resource-based policies)
    
    Returns:
        Policy statement dictionary
    """
    statement = {
        "Effect": effect,
        "Action": actions,
        "Resource": resources
    }
    
    if conditions:
        statement["Condition"] = conditions
    
    if principals:
        statement["Principal"] = principals
    
    return statement


def create_policy_document(statements: List[Dict[str, Any]], version: str = "2012-10-17"):
    """Helper function to create a complete policy document.
    
    Args:
        statements: List of policy statements
        version: Policy language version
    
    Returns:
        Complete policy document dictionary
    """
    return {
        "Version": version,
        "Statement": statements
    }


def create_lambda_execution_policy():
    """Helper function to create Lambda basic execution policy.
    
    Returns:
        Policy document for Lambda execution
    """
    statement = create_policy_statement(
        effect="Allow",
        actions=[
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ],
        resources=["arn:aws:logs:*:*:*"]
    )
    
    return create_policy_document([statement])


def create_s3_access_policy(bucket_arn: str, actions: Optional[List[str]] = None):
    """Helper function to create S3 bucket access policy.
    
    Args:
        bucket_arn: ARN of the S3 bucket
        actions: List of S3 actions to allow
    
    Returns:
        Policy document for S3 access
    """
    if actions is None:
        actions = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
    
    statement = create_policy_statement(
        effect="Allow",
        actions=actions,
        resources=[f"{bucket_arn}/*"]
    )
    
    return create_policy_document([statement])


def create_dynamodb_access_policy(table_arn: str, actions: Optional[List[str]] = None):
    """Helper function to create DynamoDB table access policy.
    
    Args:
        table_arn: ARN of the DynamoDB table
        actions: List of DynamoDB actions to allow
    
    Returns:
        Policy document for DynamoDB access
    """
    if actions is None:
        actions = [
            "dynamodb:GetItem",
            "dynamodb:PutItem",
            "dynamodb:UpdateItem",
            "dynamodb:DeleteItem",
            "dynamodb:Query",
            "dynamodb:Scan"
        ]
    
    statement = create_policy_statement(
        effect="Allow",
        actions=actions,
        resources=[table_arn, f"{table_arn}/*"]
    )
    
    return create_policy_document([statement])


def create_acm_pca_access_policy(ca_arn: str = "*"):
    """Helper function to create ACM Private CA access policy.
    
    Args:
        ca_arn: ARN of the Certificate Authority (default: all)
    
    Returns:
        Policy document for ACM PCA access
    """
    statement = create_policy_statement(
        effect="Allow",
        actions=[
            "acm-pca:IssueCertificate",
            "acm-pca:GetCertificate",
            "acm-pca:DescribeCertificateAuthority",
            "acm-pca:ListCertificateAuthorities",
            "acm-pca:GetCertificateAuthorityCertificate"
        ],
        resources=[ca_arn]
    )
    
    return create_policy_document([statement])
