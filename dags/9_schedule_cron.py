from airflow.sdk import dag, task
from pendulum import datetime
from airflow.timetables.trigger import CronTriggerTimetable

@dag(
        dag_id= "corn_schedule_dag",
        start_date = datetime(year=2026, month=2, day=25, tz="Asia/Kathmandu"),
        schedule=CronTriggerTimetable("0 16 * * Mon-FRI", timezone="Asia/Kathmandu"),
        end_date=datetime(year=2026, month=3, day=6, tz="Asia/Kathmandu"),
        is_paused_upon_creation=False,
        catchup=True
)
def corn_schedule_dag():

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
corn_schedule_dag = corn_schedule_dag()