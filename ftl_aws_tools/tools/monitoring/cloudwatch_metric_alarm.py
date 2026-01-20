#!/usr/bin/env python3
from typing import Optional, Dict, Any, List

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class CloudWatchAlarm(AutomationTool):
    name = "cloudwatch_metric_alarm"
    module = "cloudwatch_metric_alarm"
    category = "aws_monitoring"
    description = "Manage AWS CloudWatch metric alarms"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(
        self,
        name: str,
        state: str = "present",
        metric_name: Optional[str] = None,
        namespace: Optional[str] = None,
        statistic: Optional[str] = None,
        comparison: Optional[str] = None,
        threshold: Optional[float] = None,
        period: Optional[int] = None,
        evaluation_periods: Optional[int] = None,
        unit: Optional[str] = None,
        description: Optional[str] = None,
        dimensions: Optional[Dict[str, str]] = None,
        alarm_actions: Optional[List[str]] = None,
        ok_actions: Optional[List[str]] = None,
        insufficient_data_actions: Optional[List[str]] = None,
        treat_missing_data: Optional[str] = None,
        evaluate_low_sample_count_percentile: Optional[str] = None,
        datapoints_to_alarm: Optional[int] = None,
        extended_statistic: Optional[str] = None,
        metrics: Optional[List[Dict[str, Any]]] = None,
        tags: Optional[Dict[str, str]] = None,
        purge_tags: bool = True,
        region: Optional[str] = None,
        **kwargs
    ):
        """Manage AWS CloudWatch metric alarm.

        Args:
            name: Name of the alarm
            state: Whether the alarm should be present or absent
            metric_name: Name of the metric
            namespace: Namespace of the metric
            statistic: Statistic to apply (Average, Sum, SampleCount, Maximum, Minimum)
            comparison: Comparison operator
            threshold: Threshold value for comparison
            period: Period in seconds over which statistic is applied
            evaluation_periods: Number of periods to evaluate
            unit: Unit for the metric
            description: Description of the alarm
            dimensions: Dimensions for the metric
            alarm_actions: List of actions to execute when alarm state is reached
            ok_actions: List of actions to execute when alarm transitions to OK
            insufficient_data_actions: List of actions when insufficient data
            treat_missing_data: How to treat missing data points
            evaluate_low_sample_count_percentile: How to evaluate percentiles with low sample count
            datapoints_to_alarm: Number of datapoints within evaluation periods that must be breaching
            extended_statistic: Extended statistic (percentile)
            metrics: List of metrics for composite alarms
            tags: Dictionary of tags to apply to the alarm
            purge_tags: Remove tags not defined in module
            region: AWS region override
            **kwargs: Additional module arguments

        Returns:
            Module execution result with alarm details
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Build module arguments
        module_args = {
            "name": name,
            "state": state,
            "purge_tags": purge_tags,
        }
        
        # Add metric configuration
        if metric_name:
            module_args["metric_name"] = metric_name
        if namespace:
            module_args["namespace"] = namespace
        if statistic:
            module_args["statistic"] = statistic
        if extended_statistic:
            module_args["extended_statistic"] = extended_statistic
        
        # Add comparison and threshold
        if comparison:
            module_args["comparison"] = comparison
        if threshold is not None:
            module_args["threshold"] = threshold
        
        # Add evaluation configuration
        if period:
            module_args["period"] = period
        if evaluation_periods:
            module_args["evaluation_periods"] = evaluation_periods
        if datapoints_to_alarm:
            module_args["datapoints_to_alarm"] = datapoints_to_alarm
        
        # Add metric properties
        if unit:
            module_args["unit"] = unit
        if dimensions:
            module_args["dimensions"] = dimensions
        
        # Add description
        if description:
            module_args["description"] = description
        
        # Add actions
        if alarm_actions:
            module_args["alarm_actions"] = alarm_actions
        if ok_actions:
            module_args["ok_actions"] = ok_actions
        if insufficient_data_actions:
            module_args["insufficient_data_actions"] = insufficient_data_actions
        
        # Add data treatment
        if treat_missing_data:
            module_args["treat_missing_data"] = treat_missing_data
        if evaluate_low_sample_count_percentile:
            module_args["evaluate_low_sample_count_percentile"] = evaluate_low_sample_count_percentile
        
        # Add composite alarm metrics
        if metrics:
            module_args["metrics"] = metrics
        
        # Add tags
        if tags:
            module_args["tags"] = tags
        
        # Add region
        if region:
            module_args["region"] = region
        
        # Add any additional kwargs
        module_args.update(kwargs)

        output = self.context.run_module_locally(self.module, **module_args)

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output


def create_lambda_error_alarm(
    alarm_name: str,
    function_name: str,
    threshold: float = 1,
    period: int = 300,
    evaluation_periods: int = 2,
    alarm_actions: Optional[List[str]] = None
):
    """Helper function to create Lambda function error alarm.
    
    Args:
        alarm_name: Name of the alarm
        function_name: Name of the Lambda function
        threshold: Error count threshold
        period: Period in seconds
        evaluation_periods: Number of periods to evaluate
        alarm_actions: List of SNS topic ARNs
    
    Returns:
        Dictionary of parameters for cloudwatch_metric_alarm
    """
    params = {
        "name": alarm_name,
        "metric_name": "Errors",
        "namespace": "AWS/Lambda",
        "statistic": "Sum",
        "comparison": "GreaterThanOrEqualToThreshold",
        "threshold": threshold,
        "period": period,
        "evaluation_periods": evaluation_periods,
        "dimensions": {"FunctionName": function_name},
        "description": f"Lambda function {function_name} error count alarm"
    }
    
    if alarm_actions:
        params["alarm_actions"] = alarm_actions
    
    return params


def create_alb_target_response_time_alarm(
    alarm_name: str,
    load_balancer_name: str,
    threshold: float = 1.0,
    period: int = 300,
    evaluation_periods: int = 3,
    alarm_actions: Optional[List[str]] = None
):
    """Helper function to create ALB target response time alarm.
    
    Args:
        alarm_name: Name of the alarm
        load_balancer_name: Name of the Application Load Balancer
        threshold: Response time threshold in seconds
        period: Period in seconds
        evaluation_periods: Number of periods to evaluate
        alarm_actions: List of SNS topic ARNs
    
    Returns:
        Dictionary of parameters for cloudwatch_metric_alarm
    """
    params = {
        "name": alarm_name,
        "metric_name": "TargetResponseTime",
        "namespace": "AWS/ApplicationELB",
        "statistic": "Average",
        "comparison": "GreaterThanThreshold",
        "threshold": threshold,
        "period": period,
        "evaluation_periods": evaluation_periods,
        "dimensions": {"LoadBalancer": load_balancer_name},
        "description": f"ALB {load_balancer_name} high response time alarm"
    }
    
    if alarm_actions:
        params["alarm_actions"] = alarm_actions
    
    return params


def create_dynamodb_throttling_alarm(
    alarm_name: str,
    table_name: str,
    threshold: float = 1,
    period: int = 300,
    evaluation_periods: int = 2,
    alarm_actions: Optional[List[str]] = None
):
    """Helper function to create DynamoDB throttling alarm.
    
    Args:
        alarm_name: Name of the alarm
        table_name: Name of the DynamoDB table
        threshold: Throttling events threshold
        period: Period in seconds
        evaluation_periods: Number of periods to evaluate
        alarm_actions: List of SNS topic ARNs
    
    Returns:
        Dictionary of parameters for cloudwatch_metric_alarm
    """
    params = {
        "name": alarm_name,
        "metric_name": "ReadThrottledRequests",
        "namespace": "AWS/DynamoDB",
        "statistic": "Sum",
        "comparison": "GreaterThanOrEqualToThreshold",
        "threshold": threshold,
        "period": period,
        "evaluation_periods": evaluation_periods,
        "dimensions": {"TableName": table_name},
        "description": f"DynamoDB table {table_name} read throttling alarm"
    }
    
    if alarm_actions:
        params["alarm_actions"] = alarm_actions
    
    return params