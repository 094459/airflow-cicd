### How does this work?

> **Inspired by this blog post and code from Gary Stafford** 
>
> [DevOps for DataOps: Building a CI/CD Pipeline for Apache Airflow DAGs](https://programmaticponderings.com/2021/12/14/devops-for-dataops-building-a-ci-cd-pipeline-for-apache-airflow-dags/)
>

There are two folders. 

"mwaa-local" is a version of mwaa-local-runner that is optimised for local development, and whilst the "dags", "plugins", and "requirements" folders are there, they are not used in this particular configuration as the mounted volumes are different (see the next section)

```
├── dags
├── docker
│   ├── config
│   └── script
├── plugins
├── requirements

```

"workflows" maps to the actual directories that mwaa-local-runner will mount.

```

├── airflow_variables
│   └── variables.json
├── dags
├── git_hooks
│   ├── Notes.md
│   ├── pre-commit
│   └── pre-push
├── plugins
├── requirements
│   └── requirements.txt
├── run_tests_locally.sh
├── requirements_local_tests.txt
└── tests
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-38.pyc
    │   └── tests.cpython-38-pytest-6.2.5.pyc
    └── tests.py
```

As you can see, development is down in the workflow directory and is organised as follows:

* airflow_variables - a folder containing json files that you can use to import variables within Apache Airflow
* githooks - sample pre-commit hooks that you can use to trigger tests before pushing/committing changes
* tests - unit tests for your workflows
* run_tests_locally.sh - a bash script that runs a battery of tests to make sure your workflows meet various standards. This is only an example, you would use your own specific tests here.
* requirements_local_tests.txt - dependencies for the sample test script

The other folders "dags", "requirements, and "dags" are where development of your workflows would be done.

This entire folder structure would be stored in a git version control system like AWS CodeCommit.