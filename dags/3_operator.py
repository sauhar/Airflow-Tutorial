from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(
        dag_id= "bashoperator_dag"
)
def bashoperator_dag():

    @task.python
    def first_task():
        print("This is the first task")

    @task.python
    def second_task():
        print("This is the second task")

    
    @task.python
    def third_task():
        print("This is the third task")
    
    @task.bash
    def bash_task_modern():
        return "echo https://airflow.apache.org/"


    bash_task_oldschool = BashOperator(
    task_id="bash_task_oldschool",
    bash_command="echo https://airflow.apache.org/",
)






    # Defining the task dependencies
    first_task() >> second_task() >> third_task() >> bash_task_modern() >> bash_task_oldschool


# Registering the DAG
bashoperator_dag = bashoperator_dag()