#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class DynamoDBTable(AutomationTool):
    name = "dynamodb_table"
    module = "dynamodb_table"
    category = "aws_database"
    description = "Manage AWS DynamoDB tables for data storage"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name: str,
        state: str = "present",
        billing_mode: str = "PAY_PER_REQUEST",
        hash_key_name: Optional[str] = None,
        hash_key_type: str = "S",
        range_key_name: Optional[str] = None,
        range_key_type: str = "S",
        read_capacity: Optional[int] = None,
        write_capacity: Optional[int] = None,
        global_secondary_indexes: Optional[List[Dict[str, Any]]] = None,
        local_secondary_indexes: Optional[List[Dict[str, Any]]] = None,
        stream_specification: Optional[Dict[str, Any]] = None,
        point_in_time_recovery: bool = True,
        tags: Optional[Dict[str, str]] = None,
        wait: bool = True,
        wait_timeout: int = 600,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS DynamoDB tables.

        Args:
            name: Name of the DynamoDB table
            state: Whether the table should be present or absent
            billing_mode: Billing mode (PAY_PER_REQUEST or PROVISIONED)
            hash_key_name: Name of the hash key attribute
            hash_key_type: Data type of hash key (S, N, B)
            range_key_name: Name of the range key attribute (optional)
            range_key_type: Data type of range key (S, N, B)
            read_capacity: Read capacity units (for PROVISIONED billing)
            write_capacity: Write capacity units (for PROVISIONED billing)
            global_secondary_indexes: List of GSI definitions
            local_secondary_indexes: List of LSI definitions
            stream_specification: DynamoDB stream configuration
            point_in_time_recovery: Enable point-in-time recovery
            tags: Dictionary of tags to apply to the table
            wait: Wait for table to be available
            wait_timeout: Timeout for wait operation
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with table details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "name": name,
            "state": state,
            "billing_mode": billing_mode,
            "wait": wait,
            "wait_timeout": wait_timeout,
        }
        
        # Build attribute definitions and key schema
        attributes = []
        key_schema = []
        
        if hash_key_name:
            attributes.append({
                "AttributeName": hash_key_name,
                "AttributeType": hash_key_type
            })
            key_schema.append({
                "AttributeName": hash_key_name,
                "KeyType": "HASH"
            })
        
        if range_key_name:
            attributes.append({
                "AttributeName": range_key_name,
                "AttributeType": range_key_type
            })
            key_schema.append({
                "AttributeName": range_key_name,
                "KeyType": "RANGE"
            })
        
        if attributes:
            module_args["attributes"] = attributes
        if key_schema:
            module_args["key_schema"] = key_schema
        
        # Add capacity settings for provisioned billing
        if billing_mode == "PROVISIONED":
            if read_capacity:
                module_args["read_capacity"] = read_capacity
            if write_capacity:
                module_args["write_capacity"] = write_capacity
        
        # Add optional configurations
        if global_secondary_indexes:
            module_args["global_indexes"] = global_secondary_indexes
        if local_secondary_indexes:
            module_args["local_indexes"] = local_secondary_indexes
        if stream_specification:
            module_args["stream_specification"] = stream_specification
        if point_in_time_recovery is not None:
            module_args["point_in_time_recovery"] = point_in_time_recovery
        if tags:
            module_args["tags"] = tags
        if region:
            module_args["region"] = region
            
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output