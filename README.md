# Apache Airflow Tutorial

![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.x-017CEE?style=flat-square&logo=Apache%20Airflow&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)

A comprehensive Apache Airflow tutorial covering **17 production-ready DAGs** demonstrating essential workflow orchestration features, scheduling patterns, and modern TaskFlow API.

## Airflow Architecture

Apache Airflow follows a distributed architecture with the following core components:
```
┌─────────────────────────────────────────────────────────────────┐
│                         Airflow UI (Web Server)                 │
│                    (DAG visualization, monitoring)              │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Metadata Database                       │
│              (PostgreSQL/MySQL - stores DAG runs,               │
│               task states, connections, variables)              │
└──────────────┬──────────────────────────────┬───────────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────┐    ┌────────────────────────────────┐
│       Scheduler          │    │         Executor               │
│  (Reads DAGs, schedules  │◄──►│  (Runs tasks on workers)       │
│   tasks, monitors runs)  │    │  - Local/Sequential            │
│                          │    │  - Celery/Kubernetes/etc       │
└──────────────────────────┘    └────────────┬───────────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                         DAGs Folder                              │
│                  (Python files with DAG definitions)             │
└──────────────────────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Worker Nodes (Optional)                     │
│              (Execute tasks assigned by executor)                │
└──────────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Web Server** - Flask application providing the UI for monitoring and managing DAGs
2. **Scheduler** - Monitors DAGs, triggers task instances, and submits them to the executor
3. **Executor** - Handles task execution (LocalExecutor, CeleryExecutor, KubernetesExecutor, etc.)
4. **Metadata Database** - Stores all metadata (DAG runs, task states, connections, variables)
5. **DAGs Folder** - Directory containing Python files with DAG definitions
6. **Workers** - Processes that execute tasks (required for distributed executors like Celery)


## What You'll Learn

- **TaskFlow API** - Modern decorator-based DAG definition
- **XComs** - Inter-task communication (automatic & manual)
- **Task Dependencies** - Linear, parallel, and conditional branching
- **Advanced Scheduling** - Cron, delta triggers, incremental loading, event-based
- **Data-Driven Workflows** - Asset producers and consumers
- **DAG Orchestration** - Parent-child DAG triggering

## Project Structure
```
dags/
├── 1_first_dag.py                      # Basic DAG with TaskFlow API
├── 2_dag_versioning.py                 # DAG version management
├── 3_operator.py                       # Bash operators (modern + legacy)
├── 4_XCOMs_auto.py                     # Automatic XCom passing
├── 5_XCOMs_kwargs.py                   # Manual XCom push/pull
├── 6_parallel_tasks.py                 # Parallel task execution
├── 7_conditional_branches.py           # Branching logic
├── 8_schedule_preset.py                # Preset scheduling (@daily)
├── 9_schedule_cron.py                  # Custom cron scheduling
├── 10_schedule_delta.py                # Duration-based triggers
├── 11_incremental_load.py              # Data interval timetables
├── 12_special_event_schedule.py        # Event-driven scheduling
├── asset_13.py                         # Asset producer DAG
├── 14_asset_dependent.py               # Asset consumer DAG
├── dag_orchestrate_1.py                # Child DAG 1
├── dag_orchestrate_2.py                # Child DAG 2
└── dag_orchestrate_parent.py           # Parent orchestrator DAG
```

## Key DAGs Overview

### Foundation
- **1_first_dag.py** - Basic TaskFlow API structure with linear dependencies
- **2_dag_versioning.py** - Managing DAG evolution and version control
- **3_operator.py** - Modern `@task.bash` vs legacy `BashOperator`

### Data Passing & Dependencies
- **4_XCOMs_auto.py** - Automatic XCom passing with return values
- **4_XCOMs_kwargs.py** - Manual XCom push/pull with `ti.xcom_push()` and `ti.xcom_pull()`
- **6_parallel_tasks.py** - Fan-out pattern: `extract >> [transform_api, transform_db, transform_file] >> load`
- **7_conditional_branches.py** - `@task.branch` decorator for conditional routing

### Advanced Scheduling
- **8_schedule_preset.py** - Preset schedules (`@daily`, `@hourly`, `@weekly`)
- **9_schedule_cron.py** - Custom cron with `CronTriggerTimetable("0 16 * * Mon-FRI")`
- **10_schedule_delta.py** - Duration-based `DeltaTriggerTimetable(duration(days=5))`
- **11_incremental_load.py** - `CronDataIntervalTimetable` with `data_interval_start/end`
- **12_special_event_schedule.py** - Event-driven `EventsTimetable([date1, date2, date3])`

### Data-Driven Workflows
- **asset_13.py** - Asset producer with `@asset` decorator and URI definition
- **14_asset_dependent.py** - Asset consumer triggered by upstream asset availability

### Orchestration
- **dag_orchestrate_parent.py** - Parent DAG using `TriggerDagRunOperator`
- **dag_orchestrate_1.py & dag_orchestrate_2.py** - Child DAGs triggered by parent

> **⚠️ Note:** Enable child DAGs before triggering parent orchestrator DAG

## Quick Start

### Docker Setup (Recommended)
```bash
git clone https://github.com/sauhar/Airflow-Tutorial.git
cd Airflow-Tutorial
echo "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init
docker-compose up -d
```

Access Airflow UI at **http://localhost:8080** (username: `airflow`, password: `airflow`)

### Local Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install apache-airflow==2.x  # or: uv sync
export AIRFLOW_HOME=$(pwd)
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
airflow webserver --port 8080  # Terminal 1
airflow scheduler               # Terminal 2
```

## Key Concepts

### TaskFlow API vs Traditional Operators
```python
# Modern (Recommended)
@dag(dag_id="modern_dag")
def modern_dag():
    @task.python
    def extract():
        return {"data": [1,2,3]}
    
    transform(extract())  # Automatic XCom passing

# Traditional
dag = DAG('traditional_dag')
extract = PythonOperator(task_id='extract', python_callable=extract_func, dag=dag)
extract >> transform
```


### Scheduling Strategies

| Use Case | Schedule Type | Example |
|----------|---------------|---------|
| Daily reports | Preset | `schedule="@daily"` |
| Business hours | Cron | `CronTriggerTimetable("0 9 * * Mon-Fri")` |
| Fixed intervals | Delta | `DeltaTriggerTimetable(duration(hours=6))` |
| Incremental ETL | Data Interval | `CronDataIntervalTimetable("@hourly")` |
| Ad-hoc events | Events | `EventsTimetable([date1, date2])` |
| Data-driven | Assets | `schedule=upstream_asset` |

## Resources

- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Astronomer Academy](https://academy.astronomer.io/) - Free courses
