
#Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

import os
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
    # 'end_date': datetime(2016, 1, 1),
}

def print_hello():
 return 'Hello World'

def print_bye():
 return 'GoodBye World'

with DAG(
        dag_id=os.path.basename(__file__).replace(".py", ""),
        default_args=default_args,
        dagrun_timeout=timedelta(hours=2),
        schedule_interval=None
) as dag:

    hello_operator=PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)
    bye_operator=PythonOperator(task_id='bye_task', python_callable=print_bye, dag=dag)
    hello_operator >> bye_operator