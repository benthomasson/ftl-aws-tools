#!/usr/bin/env python3
from typing import Optional, Dict, Any

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class VPCSubnet(AutomationTool):
    name = "ec2_vpc_subnet"
    module = "ec2_vpc_subnet"
    category = "aws_networking"
    description = "Manage AWS VPC subnets"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        vpc_id: str,
        cidr: str,
        state: str = "present",
        availability_zone: Optional[str] = None,
        az: Optional[str] = None,  # Alias for availability_zone
        map_public: bool = False,
        assign_instances_ipv6: bool = False,
        ipv6_cidr: Optional[str] = None,
        outpost_arn: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        wait: bool = True,
        wait_timeout: int = 300,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS VPC subnet.

        Args:
            vpc_id: VPC ID to create subnet in
            cidr: CIDR block for the subnet
            state: Whether the subnet should be present or absent
            availability_zone: Availability zone for the subnet
            az: Alias for availability_zone
            map_public: Map public IP on launch
            assign_instances_ipv6: Assign IPv6 addresses on launch
            ipv6_cidr: IPv6 CIDR block for subnet
            outpost_arn: Outpost ARN for local zones
            tags: Dictionary of tags to apply to the subnet
            purge_tags: Remove tags not defined in module
            wait: Wait for subnet to be available
            wait_timeout: Timeout for wait operation
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with subnet details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "vpc_id": vpc_id,
            "cidr": cidr,
            "state": state,
            "map_public": map_public,
            "assign_instances_ipv6": assign_instances_ipv6,
            "purge_tags": purge_tags,
            "wait": wait,
            "wait_timeout": wait_timeout,
        }
        
        # Use az parameter or availability_zone
        az_value = az or availability_zone
        if az_value:
            module_args["az"] = az_value
        
        # Add IPv6 CIDR if specified
        if ipv6_cidr:
            module_args["ipv6_cidr"] = ipv6_cidr
        
        # Add Outpost ARN if specified
        if outpost_arn:
            module_args["outpost_arn"] = outpost_arn
        
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