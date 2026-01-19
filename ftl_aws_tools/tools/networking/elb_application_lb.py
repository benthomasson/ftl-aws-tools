#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class ApplicationLoadBalancer(AutomationTool):
    name = "elb_application_lb"
    module = "elb_application_lb"
    category = "aws_networking"
    description = "Manage AWS Application Load Balancer for HTTP/HTTPS traffic"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name: str,
        state: str = "present",
        scheme: str = "internet-facing",
        subnets: Optional[List[str]] = None,
        security_groups: Optional[List[str]] = None,
        ip_address_type: str = "ipv4",
        type: str = "application",
        deletion_protection: bool = False,
        idle_timeout: Optional[int] = None,
        access_logs_enabled: bool = False,
        access_logs_s3_bucket: Optional[str] = None,
        access_logs_s3_prefix: Optional[str] = None,
        listeners: Optional[List[Dict[str, Any]]] = None,
        tags: Optional[Dict[str, str]] = None,
        wait: bool = True,
        wait_timeout: int = 320,
        purge_listeners: bool = True,
        purge_tags: bool = True,
        enable_http2: bool = True,
        waf_fail_open: bool = False,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS Application Load Balancer.

        Args:
            name: Name of the load balancer
            state: Whether the ALB should be present or absent
            scheme: ALB scheme (internet-facing or internal)
            subnets: List of subnet IDs or names to attach to ALB
            security_groups: List of security group IDs to associate
            ip_address_type: IP address type (ipv4 or dualstack)
            type: Load balancer type (application)
            deletion_protection: Enable deletion protection
            idle_timeout: Idle timeout in seconds
            access_logs_enabled: Enable access logging
            access_logs_s3_bucket: S3 bucket for access logs
            access_logs_s3_prefix: S3 prefix for access logs
            listeners: List of listener configurations
            tags: Dictionary of tags to apply to the ALB
            wait: Wait for ALB to be active
            wait_timeout: Timeout for wait operation
            purge_listeners: Remove listeners not defined in module
            purge_tags: Remove tags not defined in module
            enable_http2: Enable HTTP/2 support
            waf_fail_open: WAF fail open setting
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with ALB details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "name": name,
            "state": state,
            "scheme": scheme,
            "type": type,
            "ip_address_type": ip_address_type,
            "deletion_protection": deletion_protection,
            "wait": wait,
            "wait_timeout": wait_timeout,
            "purge_listeners": purge_listeners,
            "purge_tags": purge_tags,
            "enable_http2": enable_http2,
            "waf_fail_open": waf_fail_open,
        }
        
        # Add subnets
        if subnets:
            module_args["subnets"] = subnets
        
        # Add security groups
        if security_groups:
            module_args["security_groups"] = security_groups
        
        # Add timeout settings
        if idle_timeout is not None:
            module_args["idle_timeout"] = idle_timeout
        
        # Add access logs configuration
        if access_logs_enabled:
            access_logs = {"enabled": True}
            if access_logs_s3_bucket:
                access_logs["s3_bucket"] = access_logs_s3_bucket
            if access_logs_s3_prefix:
                access_logs["s3_prefix"] = access_logs_s3_prefix
            module_args["access_logs"] = access_logs
        
        # Add listeners configuration
        if listeners:
            module_args["listeners"] = listeners
        
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


def create_https_listener(
    port: int = 443,
    certificate_arn: Optional[str] = None,
    ssl_policy: str = "ELBSecurityPolicy-TLS-1-2-2017-01",
    default_actions: Optional[List[Dict[str, Any]]] = None,
    rules: Optional[List[Dict[str, Any]]] = None,
    mutual_authentication: Optional[Dict[str, Any]] = None
):
    """Helper function to create HTTPS listener configuration for mTLS.
    
    Args:
        port: Listener port (default 443)
        certificate_arn: SSL certificate ARN
        ssl_policy: SSL security policy
        default_actions: Default actions for the listener
        rules: Listener rules
        mutual_authentication: Mutual TLS authentication configuration
    
    Returns:
        Listener configuration dictionary
    """
    listener = {
        "Protocol": "HTTPS",
        "Port": port,
        "SslPolicy": ssl_policy,
    }
    
    if certificate_arn:
        listener["Certificates"] = [{"CertificateArn": certificate_arn}]
    
    if default_actions:
        listener["DefaultActions"] = default_actions
    
    if rules:
        listener["Rules"] = rules
    
    # Add mutual authentication for client certificate validation
    if mutual_authentication:
        listener["MutualAuthentication"] = mutual_authentication
    
    return listener


def create_target_group_action(target_group_arn: str, action_type: str = "forward"):
    """Helper function to create target group action.
    
    Args:
        target_group_arn: ARN of target group
        action_type: Type of action (forward, redirect, fixed-response)
    
    Returns:
        Action configuration dictionary
    """
    return {
        "Type": action_type,
        "TargetGroupArn": target_group_arn
    }


def create_mtls_config(
    trust_store_arn: str,
    ignore_client_certificate_expiry: bool = False,
    mode: str = "verify"
):
    """Helper function to create mutual TLS configuration for client certificate validation.
    
    Args:
        trust_store_arn: ARN of trust store containing CA certificates
        ignore_client_certificate_expiry: Whether to ignore client cert expiry
        mode: Mutual authentication mode (verify, passthrough)
    
    Returns:
        Mutual authentication configuration dictionary
    """
    return {
        "Mode": mode,
        "TrustStoreArn": trust_store_arn,
        "IgnoreClientCertificateExpiry": ignore_client_certificate_expiry
    }