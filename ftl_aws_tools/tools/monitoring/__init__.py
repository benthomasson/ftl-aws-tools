"""AWS Monitoring Service Tools.

This module contains automation tools for AWS monitoring services:

- CloudWatch metrics and alarms
- CloudTrail logging
- AWS Config rules
- Systems Manager

Available tools:
    - cloudwatch_metric: Manage CloudWatch metrics
    - cloudwatch_alarm: Manage CloudWatch alarms
    - cloudtrail: Manage CloudTrail
    - config_rule: Manage AWS Config rules

Usage:
    with automation(tool_packages=["ftl_aws_tools.tools.monitoring"]) as ftl:
        ftl.cloudwatch_alarm(
            name="high-cpu",
            metric_name="CPUUtilization",
            threshold=80,
            comparison_operator="GreaterThanThreshold"
        )
"""

# Tool imports will be added here as tools are implemented
# from .cloudwatch_alarm import CloudWatchAlarm
# from .cloudtrail import CloudTrail

__all__ = [
    # Tool classes will be listed here
]