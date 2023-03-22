### How to deploy

1. Edit the app.py file to suit your AWS account and point to an existing MWAA environment you want to deploy your DAGs to
2. Update the mwaa_pipeline\MWAAPipeline.py with your email address for the approval process
3. Deploy the CDK stacks using the following command:

```
cdk deploy mwaa-pipeline
```

The deployment will take around 10 minutes to complete.

It will create a git repository in AWS CodeCommit. You can use this to trigger the pipeline and deploy DAGs to your MWAA environment.

**To uninstall**

```
cdk destroy mwaa-pipeline
```