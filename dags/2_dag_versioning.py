from airflow.sdk import dag, task

@dag(
        dag_id= "versioned_dag"
)
def versioned_dag():

    @task.python
    def first_task():
        print("This is the first task")

    @task.python
    def second_task():
        print("This is the second task")

    
    @task.python
    def third_task():
        print("This is the third task")

    @task.python
    def fourth_task():
        print("This is the version task. DAG version 2.0!")


    # Defining the task dependencies
    first_task() >> second_task() >> third_task() >> fourth_task()


# Registering the DAG
versioned_dag = versioned_dag()