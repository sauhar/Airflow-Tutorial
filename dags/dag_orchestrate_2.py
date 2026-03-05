from airflow.sdk import dag, task 
import os

@dag(
        dag_id="second_orchestrator_dag",
)
def second_orchestrator_dag():

    @task.python
    def first_task():
        print("This is the first task")

    @task.python
    def second_task():
        print("This is the second task")


    @task.python
    def third_task():
        print("This is the third task")
    
    
    # Defining task dependencies
    first = first_task()
    second = second_task()
    third = third_task()
    
    first >> second >> third

# Instantiating the DAG
second_orchestrator_dag()