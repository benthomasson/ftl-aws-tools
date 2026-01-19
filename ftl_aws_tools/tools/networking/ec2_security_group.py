#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class SecurityGroup(AutomationTool):
    name = "ec2_security_group"
    module = "ec2_security_group"
    category = "aws_networking"
    description = "Manage AWS EC2 security groups"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name: str,
        description: str,
        vpc_id: Optional[str] = None,
        state: str = "present",
        group_id: Optional[str] = None,
        rules: Optional[List[Dict[str, Any]]] = None,
        rules_egress: Optional[List[Dict[str, Any]]] = None,
        purge_rules: bool = True,
        purge_rules_egress: bool = True,
        purge_tags: bool = True,
        tags: Optional[Dict[str, str]] = None,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS EC2 security group.

        Args:
            name: Name of the security group
            description: Description of the security group
            vpc_id: VPC ID to create security group in
            state: Whether the security group should be present or absent
            group_id: ID of existing security group to modify
            rules: List of ingress rules
            rules_egress: List of egress rules
            purge_rules: Remove ingress rules not defined in module
            purge_rules_egress: Remove egress rules not defined in module
            purge_tags: Remove tags not defined in module
            tags: Dictionary of tags to apply to the security group
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with security group details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "name": name,
            "description": description,
            "state": state,
            "purge_rules": purge_rules,
            "purge_rules_egress": purge_rules_egress,
            "purge_tags": purge_tags,
        }
        
        # Add VPC ID
        if vpc_id:
            module_args["vpc_id"] = vpc_id
        
        # Add group ID if modifying existing group
        if group_id:
            module_args["group_id"] = group_id
        
        # Add rules
        if rules:
            module_args["rules"] = rules
        
        if rules_egress:
            module_args["rules_egress"] = rules_egress
        
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


def create_https_rule(
    port: int = 443,
    cidr_ip: Optional[str] = None,
    source_group_id: Optional[str] = None,
    description: Optional[str] = None
):
    """Helper function to create HTTPS ingress rule.
    
    Args:
        port: Port number (default 443)
        cidr_ip: CIDR block to allow access from
        source_group_id: Security group ID to allow access from
        description: Description for the rule
    
    Returns:
        Security group rule dictionary
    """
    rule = {
        "proto": "tcp",
        "ports": [port],
    }
    
    if description:
        rule["rule_desc"] = description
    
    if cidr_ip:
        rule["cidr_ip"] = cidr_ip
    elif source_group_id:
        rule["group_id"] = source_group_id
    else:
        rule["cidr_ip"] = "0.0.0.0/0"  # Default to allow from anywhere
    
    return rule


def create_http_rule(
    port: int = 80,
    cidr_ip: Optional[str] = None,
    source_group_id: Optional[str] = None,
    description: Optional[str] = None
):
    """Helper function to create HTTP ingress rule.
    
    Args:
        port: Port number (default 80)
        cidr_ip: CIDR block to allow access from
        source_group_id: Security group ID to allow access from
        description: Description for the rule
    
    Returns:
        Security group rule dictionary
    """
    rule = {
        "proto": "tcp",
        "ports": [port],
    }
    
    if description:
        rule["rule_desc"] = description
    
    if cidr_ip:
        rule["cidr_ip"] = cidr_ip
    elif source_group_id:
        rule["group_id"] = source_group_id
    else:
        rule["cidr_ip"] = "0.0.0.0/0"  # Default to allow from anywhere
    
    return rule


def create_custom_rule(
    protocol: str,
    port: int,
    cidr_ip: Optional[str] = None,
    source_group_id: Optional[str] = None,
    description: Optional[str] = None
):
    """Helper function to create custom security group rule.
    
    Args:
        protocol: Protocol (tcp, udp, icmp)
        port: Port number
        cidr_ip: CIDR block to allow access from
        source_group_id: Security group ID to allow access from
        description: Description for the rule
    
    Returns:
        Security group rule dictionary
    """
    rule = {
        "proto": protocol,
        "ports": [port],
    }
    
    if description:
        rule["rule_desc"] = description
    
    if cidr_ip:
        rule["cidr_ip"] = cidr_ip
    elif source_group_id:
        rule["group_id"] = source_group_id
    else:
        rule["cidr_ip"] = "0.0.0.0/0"  # Default to allow from anywhere
    
    return rule