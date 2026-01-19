#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class ACMPrivateCA(AutomationTool):
    name = "acm_private_ca"
    module = "acm_private_ca"
    category = "aws_security"
    description = "Manage AWS Certificate Manager Private Certificate Authority"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        state: str = "present",
        ca_type: str = "ROOT",
        key_algorithm: str = "RSA_2048",
        signing_algorithm: str = "SHA256WITHRSA",
        subject: Optional[Dict[str, str]] = None,
        validity_period: Optional[Dict[str, Any]] = None,
        usage_mode: str = "GENERAL_PURPOSE",
        tags: Optional[Dict[str, str]] = None,
        ca_certificate: Optional[str] = None,
        ca_certificate_chain: Optional[str] = None,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS ACM Private Certificate Authority.

        Args:
            state: Whether the CA should be present or absent
            ca_type: Type of CA (ROOT or SUBORDINATE)
            key_algorithm: Algorithm for CA key generation (RSA_2048, RSA_4096, EC_prime256v1, EC_secp384r1)
            signing_algorithm: Algorithm for signing certificates
            subject: CA subject information (Country, Organization, CommonName, etc.)
            validity_period: How long the CA certificate is valid
            usage_mode: CA usage mode (GENERAL_PURPOSE or SHORT_LIVED_CERTIFICATE)
            tags: Dictionary of tags to apply to the CA
            ca_certificate: CA certificate content (for installation)
            ca_certificate_chain: CA certificate chain (for installation)
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with CA details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "state": state,
            "type": ca_type,
            "key_algorithm": key_algorithm,
            "signing_algorithm": signing_algorithm,
            "usage_mode": usage_mode,
        }
        
        # Default subject for AAP metrics CA
        if subject is None:
            subject = {
                "Country": "US",
                "Organization": "Red Hat Inc",
                "OrganizationalUnit": "Ansible Analytics",
                "CommonName": "AAP Metrics CA"
            }
        module_args["subject"] = subject
        
        # Default validity period (10 years for CA)
        if validity_period is None:
            validity_period = {
                "Type": "YEARS",
                "Value": 10
            }
        module_args["validity"] = validity_period
        
        # Add optional parameters
        if tags:
            module_args["tags"] = tags
        if ca_certificate:
            module_args["certificate"] = ca_certificate
        if ca_certificate_chain:
            module_args["certificate_chain"] = ca_certificate_chain
        if region:
            module_args["region"] = region
            
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output