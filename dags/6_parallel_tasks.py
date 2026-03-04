from airflow.sdk import dag, task

@dag(
        dag_id= "parallel_dag"
)
def parallel_dag():

    @task.python
    def extract_task(**kwargs):
        ti = kwargs['ti']
        print("Extracting Data......")
        extracted_data_dict = {"api_extracted_data":[1,2,3,4,5,6],
                               "db_extracted_data":[7,8,9,10,11,12],
                               "file_extracted_data":[13,14,15,16,17,18]}
        ti.xcom_push(key="extracted_data", value=extracted_data_dict)

        

    @task.python
    def transform_task_api(**kwargs):
        ti = kwargs['ti']
        api_extracted_data = ti.xcom_pull(task_ids='extract_task', key='extracted_data')['api_extracted_data']
        print(f"API Extracted Data: {api_extracted_data}")
        transformed_api_data = [i*2 for i in api_extracted_data]
        ti.xcom_push(key="transformed_api_data", value=transformed_api_data)
    

    @task.python
    def transform_task_db(**kwargs):
        ti = kwargs['ti']
        db_extracted_data = ti.xcom_pull(task_ids='extract_task', key='extracted_data')['db_extracted_data']
        print(f"DB Extracted Data: {db_extracted_data}")
        transformed_db_data = [i*3 for i in db_extracted_data]
        ti.xcom_push(key="transformed_db_data", value=transformed_db_data)

    @task.python
    def transform_task_file(**kwargs):
        ti = kwargs['ti']
        file_extracted_data = ti.xcom_pull(task_ids='extract_task', key='extracted_data')['file_extracted_data']
        print(f"File Extracted Data: {file_extracted_data}")
        transformed_file_data = [i*4 for i in file_extracted_data]
        ti.xcom_push(key="transformed_file_data", value=transformed_file_data)

    
    @task.bash
    def load_task(**kwargs):
        ti = kwargs['ti']
        transformed_api_data = ti.xcom_pull(task_ids='transform_task_api', key='transformed_api_data')
        transformed_db_data = ti.xcom_pull(task_ids='transform_task_db', key='transformed_db_data')
        transformed_file_data = ti.xcom_pull(task_ids='transform_task_file', key='transformed_file_data')

        return f"echo 'Loaded Data: {transformed_api_data}, {transformed_db_data}, {transformed_file_data}'"


  

    # Defining the task dependencies in parallel
    extract_task() >> [transform_task_api(), transform_task_db(), transform_task_file()] >> load_task()


# Registering the DAG
parallel_dag = parallel_dag()