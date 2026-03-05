from dag_orchestrate_1 import first_orchestrator_dag
from dag_orchestrate_2 import second_orchestrator_dag
from airflow.sdk import dag
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

'''Before triggering this parent DAG, ensure that both child DAGs
are enabled in the Airflow UI. Otherwise, this parent DAG will trigger
both the DAGs but they will be in the 'queued' state and won't execute
'''


@dag(
    start_date=datetime(2024,1,1),
    schedule=None,
    catchup=False
)
def dag_orchestrate_parent():

    trigger_first = TriggerDagRunOperator(
        task_id="trigger_first_dag",
        trigger_dag_id="first_orchestrator_dag"
    )

    trigger_second = TriggerDagRunOperator(
        task_id="trigger_second_dag",
        trigger_dag_id="second_orchestrator_dag"
    )

    trigger_first >> trigger_second


dag_orchestrate_parent()