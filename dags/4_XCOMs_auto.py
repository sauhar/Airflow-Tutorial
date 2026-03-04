from airflow.sdk import dag, task

@dag(
        dag_id= "xcoms_dag_auto"
)
def xcoms_dag_auto():

    @task.python
    def first_task():
        print("Extracting data...... This is the first task")
        fetched_Data = {"data":[1,2,3,4,5,6]}
        return fetched_Data

    @task.python
    def second_task(data: dict):
        fetched_data = data.get("data", [])
        tansformed_data = [i*2 for i in fetched_data]
        return {"data": tansformed_data}
    
    @task.python
    def third_task(data:dict):
        load_data = data.get("data", [])
        return load_data



    # Defining the task dependencies
    first = first_task()
    second = second_task(first)
    third = third_task(second)



# Registering the DAG
xcoms_dag_auto = xcoms_dag_auto()