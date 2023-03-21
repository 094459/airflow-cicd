from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

import copy
import os


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['ricsue@amazon.com'],
    'email_on_failure': False,
    'email_on_retry': False
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

DAG_ID = "my_first_dag"

dag = DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description='First Apache Airflow DAG',
    schedule_interval=None,
    start_date=days_ago(2),
    catchup=False,
    tags=['aws','demo'],
)

work_dir="/tmp/airflow-goto-amsterdam"
source_file="source.txt"
destination_file="moved.txt"

#work_dir = Variable.get("work_dir")
#source_file = Variable.get("source_file")
#destination_file = Variable.get("destination_file")

create_file = BashOperator(
        task_id='create_file',
        bash_command="env ",
        dag=dag
    )

move_file = BashOperator(
        task_id='move_current_file',
        bash_command="pip list",
        dag=dag
    )

remove_file = BashOperator(
        task_id='remove_current_file',
        bash_command="java -version",
        dag=dag
    )

create_file >> move_file >> remove_file
