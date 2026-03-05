from airflow.sdk import dag, task
from pendulum import datetime
from airflow.timetables.events import EventsTimetable


special_dates = EventsTimetable(
    event_dates=[
    datetime(2026,2,25),
    datetime(2026,3,1),
    datetime(2026,3,5),
    datetime(2026,3,6),
    datetime(2026,3,25)
])

@dag(
        dag_id= "special_dates_dag",
        start_date = datetime(year=2026, month=2, day=15, tz="Asia/Kathmandu"),
        end_date=datetime(year=2026, month=3, day=30, tz="Asia/Kathmandu"),
        catchup=True,
        is_paused_upon_creation=False

)
def special_dates_dag():

    @task.python
    def special_event_task(**kwargs):
        execution_date = kwargs['logical_date']
        print(f"Running DAG for execution date: {execution_date}")
       
              
    special_event = special_event_task()
    
special_dates_dag()