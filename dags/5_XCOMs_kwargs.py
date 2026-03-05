from airflow.sdk import dag, task

@dag(
        dag_id= "xcoms_dag_manual"
)
def xcoms_dag_manual():

    @task.python
    def first_task(**kwargs):

        #Extracting 'ti'(TaskInstance) from kwargs to push data to XCom manually
        ti = kwargs['ti']
        
        print("Extracting data...... This is the first task")
        fetched_Data = {"data":[1,2,3,4,5,6]}
        ti.xcom_push(key="return_result", value=fetched_Data)
        

    @task.python
    def second_task(**kwargs):

        ti = kwargs['ti']

        fetched_data = ti.xcom_pull(task_ids='first_task', key='return_result')
        tansformed_data = [i*2 for i in fetched_data['data']]

        ti.xcom_push(key = "return_result", value=tansformed_data)
      
    
    @task.python
    def third_task(**kwargs):
        ti = kwargs['ti']
        load_data = ti.xcom_pull(task_ids='second_task', key='return_result')
        return load_data



    # Defining the task dependencies
    first = first_task()
    second = second_task()
    third = third_task()

    first >> second >> third



# Registering the DAG
xcoms_dag_manual = xcoms_dag_manual()