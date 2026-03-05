from airflow.sdk import dag, task
from pendulum import datetime

@dag(
        dag_id= "first_schedule_dag",
        start_date = datetime(year=2026, month=3, day=1, tz="Asia/Kathmandu"),
        schedule="@daily",
        is_paused_upon_creation=False,
        catchup=True
)
def first_schedule_dag():

    @task.python
    def first_task():
        print("This is the first task")

    @task.python
    def second_task():
        print("This is the second task")

    
    @task.python
    def third_task():
        print("This is the third task")



    # Defining the task dependencies
    first_task() >> second_task() >> third_task()


# Registering the DAG
first_schedule_dag = first_schedule_dag()