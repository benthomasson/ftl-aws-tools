#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class LambdaFunction(AutomationTool):
    name = "lambda"
    module = "lambda"
    category = "aws_compute"
    description = "Manage AWS Lambda functions"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name: str,
        state: str = "present",
        runtime: Optional[str] = None,
        role: Optional[str] = None,
        handler: Optional[str] = None,
        zip_file: Optional[str] = None,
        s3_bucket: Optional[str] = None,
        s3_key: Optional[str] = None,
        s3_object_version: Optional[str] = None,
        description: Optional[str] = None,
        timeout: Optional[int] = None,
        memory_size: Optional[int] = None,
        environment: Optional[Dict[str, str]] = None,
        dead_letter_config: Optional[Dict[str, str]] = None,
        tracing_config: Optional[Dict[str, str]] = None,
        kms_key_arn: Optional[str] = None,
        layers: Optional[List[str]] = None,
        vpc_config: Optional[Dict[str, Any]] = None,
        reserved_concurrency: Optional[int] = None,
        provisioned_concurrency_config: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        code_sha256: Optional[str] = None,
        image_uri: Optional[str] = None,
        package_type: str = "Zip",
        image_config: Optional[Dict[str, Any]] = None,
        architectures: Optional[List[str]] = None,
        ephemeral_storage: Optional[Dict[str, int]] = None,
        file_system_configs: Optional[List[Dict[str, str]]] = None,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS Lambda function.

        Args:
            name: Name of the Lambda function
            state: Whether the function should be present or absent
            runtime: Runtime for the function (python3.9, nodejs14.x, etc.)
            role: IAM role ARN for Lambda execution
            handler: Function handler (e.g., index.handler)
            zip_file: Path to zip file containing function code
            s3_bucket: S3 bucket containing function code
            s3_key: S3 key for function code
            s3_object_version: S3 object version for function code
            description: Description of the function
            timeout: Function timeout in seconds
            memory_size: Memory allocated to function in MB
            environment: Environment variables for the function
            dead_letter_config: Dead letter queue configuration
            tracing_config: X-Ray tracing configuration
            kms_key_arn: KMS key ARN for encryption
            layers: List of layer ARNs
            vpc_config: VPC configuration for the function
            reserved_concurrency: Reserved concurrency for the function
            provisioned_concurrency_config: Provisioned concurrency configuration
            tags: Dictionary of tags to apply to the function
            purge_tags: Remove tags not defined in module
            code_sha256: SHA256 hash of function code
            image_uri: Container image URI
            package_type: Package type (Zip or Image)
            image_config: Container image configuration
            architectures: List of supported architectures
            ephemeral_storage: Ephemeral storage configuration
            file_system_configs: List of file system configurations
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with Lambda function details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "name": name,
            "state": state,
            "purge_tags": purge_tags,
            "package_type": package_type,
        }
        
        # Add runtime and handler for Zip packages
        if package_type == "Zip":
            if runtime:
                module_args["runtime"] = runtime
            if handler:
                module_args["handler"] = handler
        
        # Add IAM role
        if role:
            module_args["role"] = role
        
        # Add code source
        if zip_file:
            module_args["zip_file"] = zip_file
        elif s3_bucket and s3_key:
            module_args["s3_bucket"] = s3_bucket
            module_args["s3_key"] = s3_key
            if s3_object_version:
                module_args["s3_object_version"] = s3_object_version
        elif image_uri:
            module_args["image_uri"] = image_uri
        
        # Add function configuration
        if description:
            module_args["description"] = description
        if timeout:
            module_args["timeout"] = timeout
        if memory_size:
            module_args["memory_size"] = memory_size
        
        # Add environment variables
        if environment:
            module_args["environment_variables"] = environment
        
        # Add dead letter config
        if dead_letter_config:
            module_args["dead_letter_config"] = dead_letter_config
        
        # Add tracing config
        if tracing_config:
            module_args["tracing_config"] = tracing_config
        
        # Add KMS key
        if kms_key_arn:
            module_args["kms_key_arn"] = kms_key_arn
        
        # Add layers
        if layers:
            module_args["layers"] = layers
        
        # Add VPC config
        if vpc_config:
            module_args["vpc_config"] = vpc_config
        
        # Add concurrency settings
        if reserved_concurrency is not None:
            module_args["reserved_concurrency"] = reserved_concurrency
        if provisioned_concurrency_config:
            module_args["provisioned_concurrency_config"] = provisioned_concurrency_config
        
        # Add container image config
        if image_config:
            module_args["image_config"] = image_config
        
        # Add architectures
        if architectures:
            module_args["architectures"] = architectures
        
        # Add ephemeral storage
        if ephemeral_storage:
            module_args["ephemeral_storage"] = ephemeral_storage
        
        # Add file system configs
        if file_system_configs:
            module_args["file_system_configs"] = file_system_configs
        
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


def create_vpc_config(subnet_ids: List[str], security_group_ids: List[str]):
    """Helper function to create VPC configuration for Lambda.
    
    Args:
        subnet_ids: List of subnet IDs
        security_group_ids: List of security group IDs
    
    Returns:
        VPC configuration dictionary
    """
    return {
        "SubnetIds": subnet_ids,
        "SecurityGroupIds": security_group_ids
    }


def create_environment_config(variables: Dict[str, str]):
    """Helper function to create environment configuration.
    
    Args:
        variables: Dictionary of environment variables
    
    Returns:
        Environment configuration dictionary
    """
    return {"Variables": variables}


def create_dead_letter_config(target_arn: str):
    """Helper function to create dead letter queue configuration.
    
    Args:
        target_arn: ARN of SQS queue or SNS topic
    
    Returns:
        Dead letter configuration dictionary
    """
    return {"TargetArn": target_arn}