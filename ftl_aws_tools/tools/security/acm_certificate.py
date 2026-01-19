#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class ACMCertificate(AutomationTool):
    name = "acm_certificate"
    module = "acm_certificate"
    category = "aws_security"
    description = "Manage AWS Certificate Manager certificates"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name_tag: Optional[str] = None,
        domain_name: Optional[str] = None,
        certificate_arn: Optional[str] = None,
        state: str = "present",
        certificate: Optional[str] = None,
        private_key: Optional[str] = None,
        certificate_chain: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS ACM certificate.

        Args:
            name_tag: Name tag for the certificate
            domain_name: Domain name for the certificate
            certificate_arn: ARN of existing certificate
            state: Whether the certificate should be present or absent
            certificate: PEM-encoded certificate body
            private_key: PEM-encoded private key
            certificate_chain: PEM-encoded certificate chain
            tags: Dictionary of tags to apply to the certificate
            purge_tags: Remove tags not defined in module
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with certificate details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "state": state,
            "purge_tags": purge_tags,
        }
        
        # Add certificate identification
        if name_tag:
            module_args["name_tag"] = name_tag
        if domain_name:
            module_args["domain_name"] = domain_name
        if certificate_arn:
            module_args["certificate_arn"] = certificate_arn
        
        # Add certificate content
        if certificate:
            module_args["certificate"] = certificate
        if private_key:
            module_args["private_key"] = private_key
        if certificate_chain:
            module_args["certificate_chain"] = certificate_chain
        
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


def upload_certificate(
    name_tag: str,
    certificate_path: str,
    private_key_path: str,
    certificate_chain_path: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None
):
    """Helper function to upload certificate from files.
    
    Args:
        name_tag: Name tag for the certificate
        certificate_path: Path to certificate file
        private_key_path: Path to private key file
        certificate_chain_path: Path to certificate chain file
        tags: Tags for the certificate
    
    Returns:
        Dictionary of parameters for acm_certificate
    """
    import os
    
    if not os.path.exists(certificate_path):
        raise FileNotFoundError(f"Certificate file not found: {certificate_path}")
    
    if not os.path.exists(private_key_path):
        raise FileNotFoundError(f"Private key file not found: {private_key_path}")
    
    with open(certificate_path, 'r') as f:
        certificate = f.read()
    
    with open(private_key_path, 'r') as f:
        private_key = f.read()
    
    params = {
        "name_tag": name_tag,
        "certificate": certificate,
        "private_key": private_key
    }
    
    if certificate_chain_path and os.path.exists(certificate_chain_path):
        with open(certificate_chain_path, 'r') as f:
            certificate_chain = f.read()
        params["certificate_chain"] = certificate_chain
    
    if tags:
        params["tags"] = tags
    
    return params