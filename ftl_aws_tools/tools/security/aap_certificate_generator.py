#!/usr/bin/env python3
from typing import Optional, Dict, Any

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class AAPCertificateGenerator(AutomationTool):
    name = "aap_certificate_generator"
    module = "aap_certificate_generator"
    category = "aws_security"
    description = "Generate client certificates for AAP installations"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        customer_id: str,
        installation_id: str,
        ca_arn: str,
        key_size: int = 2048,
        validity_period: Optional[Dict[str, Any]] = None,
        signing_algorithm: str = "SHA256WITHRSA",
        subject_additional_fields: Optional[Dict[str, str]] = None,
        store_private_key: bool = False,
        output_format: str = "pem",
        region: Optional[str] = None,
        **kwargs
    ):
        """Generate client certificate for AAP installation.

        Args:
            customer_id: Customer identifier for certificate subject
            installation_id: AAP installation identifier for certificate subject
            ca_arn: ARN of the ACM Private CA to issue certificate from
            key_size: Size of private key to generate (2048, 4096)
            validity_period: Certificate validity period configuration
            signing_algorithm: Algorithm for signing the certificate
            subject_additional_fields: Additional fields for certificate subject
            store_private_key: Whether to include private key in response
            output_format: Format for certificate output (pem, der)
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with certificate details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "customer_id": customer_id,
            "installation_id": installation_id,
            "ca_arn": ca_arn,
            "key_size": key_size,
            "signing_algorithm": signing_algorithm,
            "store_private_key": store_private_key,
            "output_format": output_format,
        }
        
        # Add validity period
        if validity_period:
            module_args["validity_period"] = validity_period
        else:
            module_args["validity_period"] = {"Type": "DAYS", "Value": 730}
        
        # Add additional subject fields
        if subject_additional_fields:
            module_args["subject_additional_fields"] = subject_additional_fields
        else:
            module_args["subject_additional_fields"] = {
                "Country": "US",
                "Organization": "Red Hat Inc",
                "OrganizationalUnit": "Ansible Analytics"
            }
        
        # Add region
        if region:
            module_args["region"] = region
        
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output


def generate_aap_certificate(
    customer_id: str,
    installation_id: str,
    ca_arn: str,
    environment: str = "production"
):
    """Helper function to generate AAP certificate with standard settings.
    
    Args:
        customer_id: Customer identifier
        installation_id: Installation identifier
        ca_arn: Certificate Authority ARN
        environment: Environment (production, staging, development)
    
    Returns:
        Dictionary of parameters for aap_certificate_generator
    """
    validity_days = 730 if environment == "production" else 90
    
    return {
        "customer_id": customer_id,
        "installation_id": installation_id,
        "ca_arn": ca_arn,
        "validity_period": {"Type": "DAYS", "Value": validity_days},
        "subject_additional_fields": {
            "Country": "US",
            "Organization": "Red Hat Inc",
            "OrganizationalUnit": "Ansible Analytics",
            "State": environment.title()
        }
    }


def generate_test_certificate(
    customer_id: str,
    installation_id: str,
    ca_arn: str
):
    """Helper function to generate test certificate with short validity.
    
    Args:
        customer_id: Customer identifier
        installation_id: Installation identifier  
        ca_arn: Certificate Authority ARN
    
    Returns:
        Dictionary of parameters for aap_certificate_generator
    """
    return {
        "customer_id": customer_id,
        "installation_id": installation_id,
        "ca_arn": ca_arn,
        "validity_period": {"Type": "DAYS", "Value": 30},
        "subject_additional_fields": {
            "Country": "US",
            "Organization": "Red Hat Inc",
            "OrganizationalUnit": "Ansible Analytics - Testing"
        }
    }