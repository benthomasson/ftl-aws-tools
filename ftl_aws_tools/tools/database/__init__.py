"""AWS Database Service Tools.

This module contains automation tools for AWS database services:

- RDS instances and clusters
- DynamoDB tables
- ElastiCache clusters
- Database subnet groups

Available tools:
    - rds_instance: Manage RDS instances
    - rds_subnet_group: Manage RDS subnet groups
    - dynamodb_table: Manage DynamoDB tables
    - elasticache_cluster: Manage ElastiCache clusters

Usage:
    with automation(tool_packages=["ftl_aws_tools.tools.database"]) as ftl:
        ftl.rds_instance(
            name="mydb",
            engine="postgres",
            instance_class="db.t3.micro",
            allocated_storage=20
        )
"""

# Tool imports will be added here as tools are implemented
# from .rds_instance import RDSInstance
# from .dynamodb_table import DynamoDBTable

__all__ = [
    # Tool classes will be listed here
]