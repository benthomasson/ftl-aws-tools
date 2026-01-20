#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class VPC(AutomationTool):
    name = "ec2_vpc_net"
    module = "ec2_vpc_net"
    category = "aws_networking"
    description = "Manage AWS Virtual Private Cloud (VPC)"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name: str,
        cidr_block: str,
        state: str = "present",
        dns_hostnames: bool = True,
        dns_support: bool = True,
        instance_tenancy: str = "default",
        multi_ok: bool = False,
        purge_cidrs: bool = False,
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        dhcp_opts_id: Optional[str] = None,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS VPC.

        Args:
            name: Name of the VPC
            cidr_block: CIDR block for the VPC
            state: Whether the VPC should be present or absent
            dns_hostnames: Enable DNS hostnames
            dns_support: Enable DNS support
            instance_tenancy: Instance tenancy (default, dedicated, host)
            multi_ok: Allow multiple VPCs with same name
            purge_cidrs: Remove CIDR blocks not specified
            tags: Dictionary of tags to apply to the VPC
            purge_tags: Remove tags not defined in module
            dhcp_opts_id: DHCP options set ID to associate
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with VPC details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "name": name,
            "cidr_block": cidr_block,
            "state": state,
            "dns_hostnames": dns_hostnames,
            "dns_support": dns_support,
            "tenancy": instance_tenancy,
            "multi_ok": multi_ok,
            "purge_cidrs": purge_cidrs,
            "purge_tags": purge_tags,
        }
        
        # Add tags
        if tags:
            module_args["tags"] = tags
        
        # Add DHCP options
        if dhcp_opts_id:
            module_args["dhcp_opts_id"] = dhcp_opts_id
        
        # Add region
        if region:
            module_args["region"] = region
        
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module_locally(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output