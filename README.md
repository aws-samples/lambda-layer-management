**Managing AWS Lambda Layers across multiple accounts and Regions**

AWS Lambda layers provide a convenient way to package libraries and other dependencies that you can use with your Lambda functions. Managing layer versions and updates across an organization with multiple functions, AWS Regions, and AWS accounts can be a complex task. There are a number of AWS services you can use to track the configuration of your Lambda functions, identify layers, and update to newer versions in chosen accounts and Regions. 
In this blog post, We explain how you can use AWS Config , AWS Systems Manager Automation  and AWS CloudFormation StackSets to streamline compliance enforcement and remediation for your non-compliant Lambda layers.

**Solution Overview**
The following architecture shows an AWS Organization structure, which includes a management account and a set of child accounts. You have common Lambda layers which are maintained from the management account. The layers are then shared with all the child accounts using the layer permission model.

Imagehere
 
We will utilize various other AWS services in this solution. Let's explore each of them and understand how they contribute to the overall solution.

AWS Config allows you to inspect, review, and assess the configuration of your AWS resources. In this solution, you will use AWS Config aggregator to search for functions that utilize the required layers and are located in specific regions and accounts. Subsequently, you will deploy AWS Config rules identify and update layers.

AWS Systems Manager Automation simplifies routine maintenance and deployment tasks for AWS resources. This blog help you create custom AWS Systems Manager document (SSM document) runbooks to remediate non-compliant resources discovered by AWS Config.

AWS CloudFormation StackSets extends the functionality of CloudFormation Stacks to help you create, update, or delete stacks across multiple accounts and AWS Regions. You can use StackSets to add a centralized remediation SSM document and deploy an AWS Config rule into multiple accounts.

**Prerequisites**
In this post, we assume that you already have AWS config setup and gathering data at organization level. If you haven’t done so, you can refer to our documentation on Multi-Account Multi-Region Data Aggregation

Additionally, you need IAM role to perform SSM automation on your behalf. To set up a service role for Automation, see the documentation.

**Solution Components**

**Identify regions and account to update lambda functions**
In this section, you will identify accounts and regions where you have outdated lambda layers. You can AWS config aggregator which is AWS Config resource type that collects AWS configuration and compliance data from various accounts and regions. You will use this information to deploy CloudFormation stack set in those regions and accounts later in this post. 
 
1.	To ensure that all accounts are being included in the Aggregator, navigate to the Aggregators section within AWS Config and select ConfigAggregator. All accounts in scope should be displayed.
2.	Next, go to the advanced queries under AWS Config and create a new query. In the query scope, select ConfigAggregator.
3.	Execute the following query to retrieve details about outdated Lambda functions. 

SELECT
  resourceId,
  configuration.functionName,
  configuration.version,
  configuration.functionArn,
  configuration.layers.arn
WHERE
  resourceType = 'AWS::Lambda::Function'
  AND configuration.layers.arn = <Outdate Lambda ARN>`

**Setup Automation for updating lambda layers**

To update a Lambda layer, the next step is to generate an SSM automation document and distribute it across multiple accounts. You can configure a Python script to update a Lambda function by using the updated layer as an input parameter. Once document is created, AWS config can refer that in remediation step. 
 
Note: Systems Manager automations are initiated under the context of a service role (or assume role). This allows the service to perform actions on your behalf. If you do not specify an assume role, Automation uses the context of the user who invoked the automation. The service role in the SSM document must have permissions to update Lambda function configuration. 

**Create AWS Config Rule to update Non-Compliant Lambdas**

AWS Config allows you to assess your AWS resources against a desired configuration state. To detect Lambda functions that are utilizing outdated layers, you can use AWS Config and create custom rules using  Guard Custom policy.  Once you identify outdated Lambda functions, you need to configure a remediation action for updating the non-compliant resources. You will use SSM document here created in previous section.
 
**Deploy the solution using AWS CloudFormation**
At this stage, we have gone through all different services and their functions within this solution. This section demonstrates the process of setting up the resources needed for this solution using the CloudFormation template. 
 
The stack creates the AWS config rule to identify outdated Lambda Layers, SSM document to update outdated lambda layer, and includes a sample Python code used in SSM document.
1.	To get started, Clone Lambda Layer Management repository.

`git clone git@ssh.gitlab.aws.dev:bajwkanw/lambdalayermanagements.git`

2.	Open the CloudFormation console and choose "Create StackSet" in the StackSets section.
3.	Upload the template file "lambdalayer.yaml" located in the "lambdalayermanagements" directory.
4.	Provide a name and description for the StackSet. In the parameters section, enter the NewLayerArn for the latest layer and the OldLayerArn for the layer you wish to replace.
5.	Manage execution based on your preference and hit next.
6.	Select Deploy new stacks and Deployment targets as per need.
7.	Specify regions and deployment options.
8.	Last acknowledge and summit.

Once the StackSet is created, AWS Config rules will be deployed to the specified accounts and regions. The rules will identify any Lambda functions using the outdated version of the Lambda layer and automatically update them using the new version.

**Conclusion**

You can centrally manage and control Lambda layer for all functions. Organizations can ensure that all their Lambda functions are using the most up-to-date version of the Layer and maintain compliance across their entire organization. The blog post discusses how to manage common Lambda layers across multiple accounts and regions in an organization using AWS Config, AWS Systems Manager Automation, and AWS CloudFormation StackSets. 
To learn more about using Lambda layers, visit the documentation, or see how layers are used in the Happy Path web application.
