"""FTL AWS Tools - Tool packages organized by AWS service categories.

This module contains AWS automation tools organized by service categories:

- compute/: EC2, Lambda, Auto Scaling tools
- storage/: S3, EBS, EFS tools  
- networking/: VPC, Subnet, Route Table tools
- database/: RDS, DynamoDB tools
- security/: IAM, Security Group tools
- monitoring/: CloudWatch, CloudTrail tools

Each category can be imported separately:
    
    with automation(tool_packages=["ftl_aws_tools.tools.compute"]) as ftl:
        ftl.ec2_instance(name="my-instance")

Or import multiple categories:

    with automation(tool_packages=[
        "ftl_aws_tools.tools.compute",
        "ftl_aws_tools.tools.networking"
    ]) as ftl:
        ftl.vpc(name="my-vpc")
        ftl.ec2_instance(name="my-instance")
"""