from airflow.sdk import dag, task
from pendulum import datetime
from airflow.timetables.interval import CronDataIntervalTimetable


@dag(
        dag_id= "incremental_load_dag",
        schedule=CronDataIntervalTimetable("@daily", timezone="Asia/Kathmandu"),
        start_date = datetime(year=2026, month=2, day=25, tz="Asia/Kathmandu"),
        end_date=datetime(year=2026, month=3, day=6, tz="Asia/Kathmandu"),
        #is_paused_upon_creation=False,
        catchup=True
)

def incremental_load_dag():

    @task.python
    def incremental_data_fetch(**kwargs):
        date_interval_starts = kwargs['data_interval_start']
        date_interval_end = kwargs['data_interval_end']
        print(f"Fetching data from {date_interval_starts} to {date_interval_end}")


    @task.bash
    def incremental_data_process():
        return "echo 'Processing incremental data from {{data_interval_start}} to {{data_interval_end}}'"
        
    #Defining the task dependencies
    incremental_data_fetch()>>incremental_data_process()

#Instantiating the DAG
incremental_load_dag()