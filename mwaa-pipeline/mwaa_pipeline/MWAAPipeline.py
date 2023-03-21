from aws_cdk import (
    # Duration,
    Stack,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_iam as iam,
    aws_s3 as s3,
    aws_sns as sns

)
import aws_cdk as cdk
from constructs import Construct

class MWAAPipeline(Stack):

    def __init__(self, scope: Construct, id: str, airflow_props,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Setup CodeCommit repo and copy initial files

        dags_bucket = f"{airflow_props['dags_s3_bucket_name']}"
        dags_bucket_arn = s3.Bucket.from_bucket_name(self, "GetDAGSbucket", f"{airflow_props['dags_s3_bucket_name']}").bucket_arn

        repo = codecommit.Repository(
            self,
            "Repository",
            repository_name=f"{airflow_props['code_repo_name']}",
            code=codecommit.Code.from_directory("repo",f"{airflow_props['branch_name']}")
        )
        cdk.CfnOutput(self, "Repository_Name", value=repo.repository_name)
       
        # Setup CodeBuild

        deploy = codebuild.Project(
            self,
            "DAGS_Deploy",
            source=codebuild.Source.code_commit(repository=repo, branch_or_ref=f"{airflow_props['branch_name']}"),
            environment=codebuild.BuildEnvironment(compute_type=codebuild.ComputeType.SMALL, privileged=True, build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_4),
            environment_variables={"BUCKET_NAME": codebuild.BuildEnvironmentVariable(value=dags_bucket)},
            build_spec=codebuild.BuildSpec.from_object(
                dict(
                    version="0.2",
                    phases={
                        "pre_build": {"commands": ["aws --version", "echo $BUCKET_NAME"]},
                        "build": {"commands": ["cd dags", "aws s3 sync . s3://$BUCKET_NAME/dags/ --delete"]},
                    },
                )
            ),
        )

        test = codebuild.Project(
            self,
            "DAGS_Test",
            source=codebuild.Source.code_commit(repository=repo, branch_or_ref=f"{airflow_props['branch_name']}"),
            environment=codebuild.BuildEnvironment(compute_type=codebuild.ComputeType.SMALL, privileged=True, build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_4),
            environment_variables={"BUCKET_NAME": codebuild.BuildEnvironmentVariable(value=dags_bucket)},
            build_spec=codebuild.BuildSpec.from_object(
                dict(
                    version="0.2",
                    phases={
                        "pre_build": {"commands": ["aws --version", "echo $BUCKET_NAME"]},
                        "build": {"commands": ["echo 'Testing'"]},
                    },
                )
            ),
        )

        # Add permissions so that it can write to our DAGs folder

        deploy.add_to_role_policy(iam.PolicyStatement(
            actions=[
                "s3:*"], 
            effect=iam.Effect.ALLOW,
            resources=[ f"{dags_bucket_arn}", f"{dags_bucket_arn}/*" ],)
            )

        # Setup CodePipeline steps

        source_output = codepipeline.Artifact()
        test_output = codepipeline.Artifact()
        deploy_output = codepipeline.Artifact("AirflowImageBuild")

        pipeline = codepipeline.Pipeline(
            self,
            "MWAA_Pipeline"
        )
        
        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=repo,
            output=source_output,
            branch=f"{airflow_props['branch_name']}"
        )

        test_action = codepipeline_actions.CodeBuildAction(
            action_name="Test",
            input=source_output,
            project=test,
            outputs=[test_output]
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="Build_action",
            input=source_output,
            project=deploy,
            outputs=[deploy_output]
        )
        pipeline.add_stage(
            stage_name="Source",
            actions=[source_action]
        )

        pipeline.add_stage(
            stage_name="Testing",
            actions=[test_action]
        )

        approval = pipeline.add_stage(
            stage_name="Approve")
        manual_approval_action = codepipeline_actions.ManualApprovalAction(
            action_name="Approve",
            notification_topic=sns.Topic(self, "Topic"), 
            notify_emails=["ricsue@amazon.com"],
            additional_information="additional info",
            external_entity_link="https://dev.to/aws/aws-open-source-news-and-updates-reference-5clm")
        approval.add_action(manual_approval_action)

        pipeline.add_stage(
            stage_name="Deployment",
            actions=[build_action]
        )
