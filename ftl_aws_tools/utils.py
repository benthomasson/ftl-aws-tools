"""AWS-specific utilities for FTL AWS Tools.

This module provides AWS-specific utility functions and classes for use
across AWS automation tools. It handles common AWS operations like
credential management, region detection, and resource tagging.
"""

import os
import boto3
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError, NoCredentialsError


class AWSConfig:
    """AWS configuration helper for FTL automation tools.
    
    Provides standardized AWS configuration handling including:
    - Region detection and validation
    - Credential validation  
    - Common AWS session management
    - Default tag management
    """
    
    def __init__(self, region: Optional[str] = None, profile: Optional[str] = None):
        """Initialize AWS configuration.
        
        Args:
            region: AWS region (defaults to environment/config)
            profile: AWS profile name (defaults to default profile)
        """
        self.region = region or self._detect_region()
        self.profile = profile
        self._session = None
        
    def _detect_region(self) -> str:
        """Detect AWS region from environment or config."""
        # Check environment variable
        region = os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION')
        if region:
            return region
            
        # Try to get from boto3 session
        try:
            session = boto3.Session()
            region = session.region_name
            if region:
                return region
        except Exception:
            pass
            
        # Default to us-east-1
        return 'us-east-1'
        
    @property 
    def session(self) -> boto3.Session:
        """Get or create boto3 session."""
        if self._session is None:
            if self.profile:
                self._session = boto3.Session(
                    profile_name=self.profile,
                    region_name=self.region
                )
            else:
                self._session = boto3.Session(region_name=self.region)
        return self._session
        
    def validate_credentials(self) -> bool:
        """Validate AWS credentials are available and working.
        
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            sts = self.session.client('sts')
            sts.get_caller_identity()
            return True
        except (ClientError, NoCredentialsError):
            return False
            
    def get_account_id(self) -> Optional[str]:
        """Get current AWS account ID.
        
        Returns:
            AWS account ID or None if unable to retrieve
        """
        try:
            sts = self.session.client('sts')
            response = sts.get_caller_identity()
            return response.get('Account')
        except (ClientError, NoCredentialsError):
            return None


def get_aws_region() -> str:
    """Get current AWS region.
    
    Returns:
        Current AWS region name
    """
    config = AWSConfig()
    return config.region


def get_aws_account_id() -> Optional[str]:
    """Get current AWS account ID.
    
    Returns:
        AWS account ID or None if unable to retrieve
    """
    config = AWSConfig()
    return config.get_account_id()


def get_default_tags() -> Dict[str, str]:
    """Get default tags for AWS resources.
    
    Returns:
        Dictionary of default tags to apply to resources
    """
    return {
        'ManagedBy': 'FTL-Automation',
        'CreatedBy': 'ftl-aws-tools',
    }


def merge_tags(resource_tags: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Merge resource-specific tags with default tags.
    
    Args:
        resource_tags: Resource-specific tags to merge
        
    Returns:
        Merged tags dictionary
    """
    tags = get_default_tags()
    if resource_tags:
        tags.update(resource_tags)
    return tags


def format_ansible_tags(tags: Dict[str, str]) -> Dict[str, Any]:
    """Format tags for Ansible AWS modules.
    
    Many Ansible AWS modules expect tags in specific formats.
    
    Args:
        tags: Tags dictionary
        
    Returns:
        Tags formatted for Ansible modules
    """
    return {
        'resource_tags': tags,
        'purge_tags': False  # Don't remove existing tags by default
    }


def build_module_args(
    base_args: Dict[str, Any], 
    region: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """Build standardized module arguments for AWS tools.
    
    Args:
        base_args: Tool-specific arguments
        region: AWS region override
        tags: Resource tags
        dry_run: Enable Ansible check mode
        
    Returns:
        Complete module arguments dictionary
    """
    args = base_args.copy()
    
    # Add region if specified
    if region:
        args['region'] = region
    elif 'region' not in args:
        args['region'] = get_aws_region()
        
    # Add tags if specified
    if tags:
        merged_tags = merge_tags(tags)
        args.update(format_ansible_tags(merged_tags))
        
    # Add check mode for dry run
    if dry_run:
        args['_ansible_check_mode'] = True
        
    return args


def validate_aws_resource_name(name: str, max_length: int = 255) -> bool:
    """Validate AWS resource name follows AWS naming conventions.
    
    Args:
        name: Resource name to validate
        max_length: Maximum allowed length
        
    Returns:
        True if name is valid, False otherwise
    """
    if not name or len(name) > max_length:
        return False
        
    # Basic validation - alphanumeric, hyphens, underscores
    # Each AWS service has specific rules, but this covers most cases
    import re
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, name))


def get_availability_zones(region: Optional[str] = None) -> list:
    """Get list of availability zones for a region.
    
    Args:
        region: AWS region (defaults to current region)
        
    Returns:
        List of availability zone names
    """
    config = AWSConfig(region=region)
    
    try:
        ec2 = config.session.client('ec2')
        response = ec2.describe_availability_zones()
        return [az['ZoneName'] for az in response['AvailabilityZones'] 
                if az['State'] == 'available']
    except ClientError:
        return []