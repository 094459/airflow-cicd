### How to deploy

1. Edit the app.py file to suit your AWS account and set unique S3 bucket details
2. Deploy the CDK stacks using the following command:

```
cdk deploy mwaa-devops-vpc
cdk deploy mwaa-devops-dev-environment
```

The deployment will take around 25-30 minutes to complete.

**To uninstall**

You will need to manually delete the S3 bucket that was created for your DAGs, and then use CDK to uninstall

```
cdk destroy mwaa-devops-dev-environment
cdk destroy mwaa-devops-vpc
```