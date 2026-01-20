#!/usr/bin/env python3
from typing import Optional, Dict, Any

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class InternetGateway(AutomationTool):
    name = "ec2_vpc_igw"
    module = "ec2_vpc_igw"
    category = "aws_networking"
    description = "Manage AWS VPC Internet Gateway"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        vpc_id: str,
        state: str = "present",
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS VPC Internet Gateway.

        Args:
            vpc_id: VPC ID to attach gateway to
            state: Whether the gateway should be present or absent
            tags: Dictionary of tags to apply to the gateway
            purge_tags: Remove tags not defined in module
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with gateway details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "vpc_id": vpc_id,
            "state": state,
            "purge_tags": purge_tags,
        }
        
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