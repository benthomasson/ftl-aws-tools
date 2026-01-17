
# FTL AWS Tools

AWS automation tools for the FTL Automation framework. This package provides a comprehensive set of AWS service automation tools organized by service categories for easy discovery and logical grouping.

## Overview

FTL AWS Tools extends the [FTL Automation](https://github.com/your-org/ftl-automation) framework with AWS-specific automation capabilities. Tools are built on Ansible's AWS collection modules and provide a Python API for infrastructure automation.

## Features

- **Service-organized**: Tools grouped by AWS service categories (compute, storage, networking, etc.)
- **Dry-run support**: Preview changes before execution with `--dry-run` mode
- **Consistent API**: Standardized parameter naming following ftl-automation patterns
- **Rich output**: Formatted console output with progress indicators
- **AWS integration**: Built on Ansible's official AWS collection modules
- **Credential management**: Automatic AWS credential detection and region handling

## Installation

### From Source
```bash
git clone https://github.com/your-org/ftl-aws-tools
cd ftl-aws-tools
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/your-org/ftl-aws-tools
cd ftl-aws-tools
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
import ftl_automation

# Use specific AWS service categories
with ftl_automation.automation(
    tool_packages=["ftl_aws_tools.tools.compute"],
    tools=["ec2_instance", "ec2_security_group"]
) as ftl:
    # Create security group
    sg_result = ftl.ec2_security_group(
        name="web-sg",
        description="Web server security group", 
        vpc_id="vpc-12345",
        rules=[
            {"proto": "tcp", "ports": ["80", "443"], "cidr_ip": "0.0.0.0/0"}
        ]
    )
    
    # Launch EC2 instance
    ftl.ec2_instance(
        name="web-server",
        image_id="ami-12345",
        instance_type="t3.micro",
        security_groups=[sg_result["group_id"]]
    )
```

### Multi-Service Automation

```python
# Combine multiple AWS service categories
with ftl_automation.automation(
    tool_packages=[
        "ftl_aws_tools.tools.networking",
        "ftl_aws_tools.tools.compute", 
        "ftl_aws_tools.tools.storage"
    ]
) as ftl:
    # Create VPC infrastructure
    vpc = ftl.vpc(name="my-vpc", cidr="10.0.0.0/16")
    subnet = ftl.subnet(
        vpc_id=vpc["vpc"]["id"],
        cidr="10.0.1.0/24",
        availability_zone="us-east-1a"
    )
    
    # Create storage
    ftl.s3_bucket(name="my-app-bucket")
    
    # Launch compute resources
    ftl.ec2_instance(
        name="app-server",
        subnet_id=subnet["subnet"]["id"],
        image_id="ami-12345"
    )
```

### Dry Run Mode

```python
# Preview changes without executing them
with ftl_automation.automation(
    dry_run=True,  # Enable dry run for entire context
    tool_packages=["ftl_aws_tools.tools.compute"]
) as ftl:
    ftl.ec2_instance(name="test-instance", image_id="ami-12345")
    # Shows what would be created without actually creating it
```

## Tool Categories

### 🖥️ Compute Tools
**Package**: `ftl_aws_tools.tools.compute`

- `ec2_instance` - Manage EC2 instances
- `ec2_security_group` - Manage security groups
- `ec2_key` - Manage EC2 key pairs
- `ec2_ami` - Manage AMIs
- `lambda_function` - Manage Lambda functions

### 💾 Storage Tools  
**Package**: `ftl_aws_tools.tools.storage`

- `s3_bucket` - Manage S3 buckets
- `s3_object` - Manage S3 objects
- `ebs_volume` - Manage EBS volumes
- `efs_filesystem` - Manage EFS file systems

### 🌐 Networking Tools
**Package**: `ftl_aws_tools.tools.networking`

- `vpc` - Manage VPCs
- `subnet` - Manage subnets
- `internet_gateway` - Manage internet gateways
- `route_table` - Manage route tables
- `nat_gateway` - Manage NAT gateways
- `elastic_ip` - Manage Elastic IPs

### 🗄️ Database Tools
**Package**: `ftl_aws_tools.tools.database`

- `rds_instance` - Manage RDS instances
- `rds_subnet_group` - Manage RDS subnet groups
- `dynamodb_table` - Manage DynamoDB tables

### 🔒 Security Tools
**Package**: `ftl_aws_tools.tools.security`

- `iam_role` - Manage IAM roles
- `iam_policy` - Manage IAM policies
- `iam_user` - Manage IAM users
- `security_group` - Manage security groups

### 📊 Monitoring Tools
**Package**: `ftl_aws_tools.tools.monitoring`

- `cloudwatch_alarm` - Manage CloudWatch alarms
- `cloudwatch_metric` - Manage CloudWatch metrics
- `cloudtrail` - Manage CloudTrail

## Prerequisites

### AWS Credentials
Configure AWS credentials using any of these methods:

```bash
# AWS CLI
aws configure

# Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# IAM roles (recommended for EC2/Lambda)
# Attach appropriate IAM role to your compute resource
```

### Required Permissions
Tools require appropriate AWS IAM permissions for the services being managed. Example policies:

- **EC2 Full Access** for compute tools
- **S3 Full Access** for storage tools  
- **VPC Full Access** for networking tools
- **RDS Full Access** for database tools
- **IAM Full Access** for security tools

### Ansible Collections
Install required Ansible collections:

```bash
ansible-galaxy collection install amazon.aws community.aws
```

## Configuration

### Region Configuration
```python
# Set region in code
with ftl_automation.automation(
    tool_packages=["ftl_aws_tools.tools.compute"],
    secrets=["AWS_REGION=us-west-2"]
) as ftl:
    # Tools will use us-west-2
```

### Default Tags
All resources are automatically tagged:
```python
# Default tags applied to all resources
{
    'ManagedBy': 'FTL-Automation',
    'CreatedBy': 'ftl-aws-tools'
}
```

Add custom tags:
```python
ftl.ec2_instance(
    name="my-instance",
    tags={
        'Environment': 'production',
        'Project': 'web-app'
    }
)
```

## Tool Development

### Creating Custom AWS Tools

```python
from ftl_automation import AutomationTool
from ftl_aws_tools.utils import build_module_args
import faster_than_light as ftl

class MyAWSTool(AutomationTool):
    name = "my_aws_tool"
    category = "aws_custom"
    description = "My custom AWS automation tool"
    
    def __call__(self, name: str, state: str = "present", **kwargs):
        # Build standardized module args with AWS defaults
        module_args = build_module_args(
            base_args={"name": name, "state": state, **kwargs},
            dry_run=getattr(self.context, 'dry_run', False)
        )
        
        return ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "amazon.aws.my_aws_module",  # Ansible module name
            self.context.gate_cache,
            module_args=module_args,
            # ... standard parameters
        )
```

### Tool Standards

Follow these conventions when creating AWS tools:

1. **Parameter Naming**:
   - Use `name` for resource names
   - Use `state` for desired state (`present`/`absent`)
   - Use `tags` for resource tags

2. **Dry Run Support**:
   ```python
   module_args = build_module_args(
       base_args=my_args,
       dry_run=getattr(self.context, 'dry_run', False)
   )
   ```

3. **Error Handling**:
   ```python
   from ftl_tools.utils import display_results
   
   # Display results with error handling
   display_results(output, self.context.console)
   ```

## Testing

Run tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=ftl_aws_tools tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-aws-tool`
3. Add your tool following the existing patterns
4. Add tests for your tool
5. Update documentation
6. Submit a pull request

### Development Setup

```bash
git clone https://github.com/your-org/ftl-aws-tools
cd ftl-aws-tools
pip install -e ".[dev]"
pre-commit install
```

## Dependencies

- **ftl-automation**: Core automation framework
- **faster-than-light**: FTL engine
- **boto3**: AWS SDK for Python
- **rich**: Console formatting
- **ansible**: Core Ansible collections

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/ftl-aws-tools/issues)
- **Documentation**: [Read the Docs](https://ftl-aws-tools.readthedocs.io/)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/ftl-aws-tools/discussions)

## Roadmap

- [ ] Additional AWS service tools (Route53, CloudFormation, etc.)
- [ ] Multi-region support and resource discovery
- [ ] Integration with AWS Organizations
- [ ] Advanced tagging and cost management tools
- [ ] AWS Config and compliance tools

