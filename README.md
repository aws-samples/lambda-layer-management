# Managing AWS Lambda Layers across multiple accounts and Regions
AWS Lambda layers provide a convenient way to package libraries and other dependencies that you can use with your Lambda functions. Managing layer versions and updates across an organization with multiple functions, AWS Regions, and AWS accounts can be a complex task. There are a number of AWS services you can use to track the configuration of your Lambda functions, identify layers, and update to newer versions in chosen accounts and Regions. In this blog post, We explain how you can use AWS Config , AWS Systems Manager Automation and AWS CloudFormation StackSets to streamline compliance enforcement and remediation for your non-compliant Lambda layers.

# Deploy the solution using AWS CloudFormation
At this stage, we have gone through all different services and their functions within this solution. This section demonstrates the process of setting up the resources needed for this solution using the CloudFormation template.

Follow the procedures below to create and deploy CloudFormation StackSets from your management account for automatic remediation:

1. Run the following command in CloudShell to clone the GitHub repository:

    ```bash
    git clone https://github.com/aws-samples/lambda-layer-management.git
    ```

2. Run the following CLI command to upload your template and create the stack set container.

    ```bash
    aws cloudformation create-stack-set \
    --stack-set-name layers-remediation-stackset \
    --template-body file://lambda-layer-management/layer_manager.yaml
    ```

3. Run the following CLI command to add stack instances in the desired accounts and regions to your CloudFormation StackSets. Replace the account IDs, regions, and parameters before you execute this command. You can refer to the syntax in the AWS CLI Command Reference. “NewLayerArn” is the ARN for your updated Lambda layer, while “OldLayerArn” is the original Lambda layer ARN.

    ```bash
      aws cloudformation create-stack-instances
      --stack-set-name layers-remediation-stackset
      --accounts <LIST_OF_ACCOUNTS>
      --regions <YOUR_REGIONS>
      --parameter-overrides ParameterKey=NewLayerArn,ParameterValue='<NEW_LAYER_ARN>' ParameterKey=OldLayerArn,ParameterValue='=<OLD_LAYER_ARN>'
    ```

4. Run the following CLI command to verify that the stack instances were created successfully. The operation ID should be returned as part of the output from step 3.

    ```bash
      aws cloudformation describe-stack-set-operation
      --stack-set-name layers-remediation-stackset
      --operation-id <OPERATION_ID>
    ```

This CloudFormation Stackset will deploy an EventBridge Scheduler that immediately triggers the AWS Config custom rule for evaluation. This rule, written in AWS CloudFormation Guard, will detect all the Lambda functions in the respective member accounts currently using the outdated Lambda layer version. By leveraging the Auto Remediation feature of AWS Config, SSM automation document will be executed against each non-compliant Lambda function to update them with the new layer version.

## Cleaning up
Refer to the documentation for instructions on [deleting all the created stack instances](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stackinstances-delete.html) from your account. After, proceed to [delete the CloudFormation StackSet](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-delete.html).


