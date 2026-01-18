#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class KMSKey(AutomationTool):
    name = "kms_key"
    module = "kms_key"
    category = "aws_security"
    description = "Manage AWS KMS keys for encryption and access control"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        alias: Optional[str] = None,
        key_id: Optional[str] = None,
        state: str = "present",
        description: Optional[str] = None,
        enabled: bool = True,
        multi_region: bool = False,
        enable_key_rotation: Optional[bool] = None,
        key_spec: str = "SYMMETRIC_DEFAULT",
        key_usage: str = "ENCRYPT_DECRYPT",
        pending_window: Optional[int] = None,
        policy: Optional[Dict[str, Any]] = None,
        grants: Optional[List[Dict[str, Any]]] = None,
        purge_grants: bool = False,
        tags: Optional[Dict[str, str]] = None,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS KMS keys.

        Args:
            alias: An alias for the key (with or without 'alias/' prefix)
            key_id: Key ID or ARN of the key 
            state: Whether the key should be present or absent
            description: A description of the KMS key
            enabled: Whether the key is enabled
            multi_region: Whether to create a multi-Region primary key
            enable_key_rotation: Whether to enable automatic annual key rotation
            key_spec: Type of KMS key (SYMMETRIC_DEFAULT, RSA_2048, etc.)
            key_usage: Cryptographic operations (ENCRYPT_DECRYPT or SIGN_VERIFY)
            pending_window: Days between deletion request and actual deletion (7-30)
            policy: Key policy as a dictionary
            grants: List of grants to apply to the key
            purge_grants: Whether to remove grants not in the list
            tags: Dictionary of tags to apply to the key
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with key details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments - FTL handles JSON serialization automatically
        module_args = {
            "state": state,
            "enabled": enabled,
            "multi_region": multi_region, 
            "key_spec": key_spec,
            "key_usage": key_usage,
            "purge_grants": purge_grants,
        }
        
        # Add optional parameters
        if alias:
            module_args["alias"] = alias
        if key_id:
            module_args["key_id"] = key_id
        if description:
            module_args["description"] = description
        if enable_key_rotation is not None:
            module_args["enable_key_rotation"] = enable_key_rotation
        if pending_window is not None:
            module_args["pending_window"] = pending_window
        if policy:
            module_args["policy"] = policy
        if grants:
            module_args["grants"] = grants
        if tags:
            module_args["tags"] = tags
        if region:
            module_args["region"] = region
            
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output
