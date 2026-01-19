#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class S3Bucket(AutomationTool):
    name = "s3_bucket"
    module = "s3_bucket"
    category = "aws_storage"
    description = "Manage AWS S3 buckets"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name: str,
        state: str = "present",
        policy: Optional[Dict[str, Any]] = None,
        requester_pays: bool = False,
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        versioning: Optional[bool] = None,
        encryption: Optional[str] = None,
        encryption_key_id: Optional[str] = None,
        bucket_key_enabled: bool = False,
        public_access_block: Optional[Dict[str, bool]] = None,
        delete_public_access_block: bool = False,
        object_lock_enabled: bool = False,
        acl: Optional[str] = None,
        validate_bucket_name: bool = True,
        dualstack: bool = False,
        accelerate: bool = False,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS S3 bucket.

        Args:
            name: Name of the S3 bucket
            state: Whether the bucket should be present or absent
            policy: Bucket policy as a dictionary
            requester_pays: Enable requester pays
            tags: Dictionary of tags to apply to the bucket
            purge_tags: Remove tags not defined in module
            versioning: Enable versioning (None=no change, True=enable, False=suspend)
            encryption: Encryption type (AES256, aws:kms, aws:kms:dsse)
            encryption_key_id: KMS key ID for encryption
            bucket_key_enabled: Enable S3 bucket key for KMS
            public_access_block: Public access block settings
            delete_public_access_block: Delete public access block configuration
            object_lock_enabled: Enable object lock (immutable)
            acl: Access control list setting
            validate_bucket_name: Validate bucket name format
            dualstack: Use dualstack endpoint
            accelerate: Enable transfer acceleration
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with bucket details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "name": name,
            "state": state,
            "requester_pays": requester_pays,
            "purge_tags": purge_tags,
            "bucket_key_enabled": bucket_key_enabled,
            "delete_public_access_block": delete_public_access_block,
            "object_lock_enabled": object_lock_enabled,
            "validate_bucket_name": validate_bucket_name,
            "dualstack": dualstack,
            "accelerate_enabled": accelerate,
        }
        
        # Add bucket policy
        if policy:
            module_args["policy"] = policy
        
        # Add tags
        if tags:
            module_args["tags"] = tags
        
        # Add versioning
        if versioning is not None:
            module_args["versioning"] = versioning
        
        # Add encryption
        if encryption:
            module_args["encryption"] = encryption
        if encryption_key_id:
            module_args["encryption_key_id"] = encryption_key_id
        
        # Add public access block
        if public_access_block:
            module_args["public_access"] = public_access_block
        
        # Add ACL
        if acl:
            module_args["acl"] = acl
        
        # Add region
        if region:
            module_args["region"] = region
        
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output


def create_public_access_block(
    block_public_acls: bool = True,
    block_public_policy: bool = True,
    ignore_public_acls: bool = True,
    restrict_public_buckets: bool = True
):
    """Helper function to create public access block configuration.
    
    Args:
        block_public_acls: Block public ACLs
        block_public_policy: Block public bucket policies
        ignore_public_acls: Ignore public ACLs
        restrict_public_buckets: Restrict public bucket policies
    
    Returns:
        Public access block configuration dictionary
    """
    return {
        "block_public_acls": block_public_acls,
        "block_public_policy": block_public_policy,
        "ignore_public_acls": ignore_public_acls,
        "restrict_public_buckets": restrict_public_buckets
    }


def create_bucket_policy_statement(
    effect: str,
    actions: List[str],
    resources: List[str],
    principals: Optional[Dict[str, Any]] = None,
    conditions: Optional[Dict[str, Any]] = None
):
    """Helper function to create a bucket policy statement.
    
    Args:
        effect: Allow or Deny
        actions: List of S3 actions
        resources: List of resource ARNs
        principals: Principal specification
        conditions: Condition block
    
    Returns:
        Policy statement dictionary
    """
    statement = {
        "Effect": effect,
        "Action": actions,
        "Resource": resources
    }
    
    if principals:
        statement["Principal"] = principals
    
    if conditions:
        statement["Condition"] = conditions
    
    return statement


def create_bucket_policy(statements: List[Dict[str, Any]]):
    """Helper function to create a complete bucket policy.
    
    Args:
        statements: List of policy statements
    
    Returns:
        Complete bucket policy dictionary
    """
    return {
        "Version": "2012-10-17",
        "Statement": statements
    }