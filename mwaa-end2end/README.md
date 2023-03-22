### Setting up an end to end Apache Airflow pipeline

This code will help you deploy via AWS CDK and pipeline that will:

* deploy MWAA environments and supporting tools
* deploy your workflows

> **Inspired heavily by an existing AWS project**
>
> [cdk-amazon-mwaa-cicd](https://github.com/aws-samples/cdk-amazon-mwaa-cicd)
> 
> I borrowed heavily from this project but updated it to use CDKv2
> 

The CDK app creates two git repositories in AWS CodeCommit (one for infrastructure, the other for the workflows) and then creates two pipelines in AWS CodePipelines that trigger once code has been updated in the git repositories.

To deploy

1. Update the app.py with the AWS Account details you need
2. Use "cdk deploy MWAAirflowStack" the stack, which will take around 30-40 minutes. You can alter the configuration by passing in the following configuration parameters

```
cdk deploy --context vpcId=vpcid --context envName=mwaademo MWAAirflowStack 
```

* vpcId  - If you have an existing VPC that meets the MWAA requirements (perhaps you want to deploy multiple MWAA environments in the same VPC for example) you can pass in the VPCId you want to deploy into. For example, you would use --contenxt vpcId=vpc-095deff9b68f4e65f
* cidr - If you want to create a new VPC, you can define your preferred CIDR block using this parameter (otherwise a default value of 172.31.0.0/16 will be used). For example, you would use --context cidr=10.192.0.0/16
* subnetIds	- Is a comma separated list of subnets IDs where the cluster will be deployed. If you do not provide one, it will look for private subnets in the same AZ
* envName - a string that represents the name of your MWAA environment, defaulting to "MwaaEnvironment" if you do not set this. For example, --context envName=MyAirflowEnv
* envTags - allows you to set Tags for the MWAA resources, providing a json expression. For example, you would use --context envTags='{"Environment":"MyEnv","Application":"MyApp","Reason":"Airflow"}'
* environmentClass	- allows you to configure the MWAA Workers size (either mw1.small, mw1.medium, mw1.large, defaulting to mw1.small). For example, --context 	environmentClass=mw1.medium
* maxWorkers	- change the number of MWAA Max Workers, defaulting to 1. For example, --context maxWorkers=2
* webserverAccessMode	- define whether you want a public or private endpoint for your MWAA Environment (using PUBLIC_ONLY or PRIVATE_ONLY).  For example, you would use --context webserverAccessMode=PUBLIC_ONLY mode (private/public)
* secretsBackend	- configure whether you want to integrate with AWS Secrets Manager, using values Airflow or SecretsManager. For example, you would use --context secretsBackend=SecretsManager 

**To uninstall**

You will need to manually delete the S3 bucket that was created for your DAGs, and then use CDK to uninstall

```
cdk destroy MWAAirflowStack
```
