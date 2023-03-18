from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta

###############################################
# Parameters
###############################################
spark_master = "spark://master:7077"
# csv_file = "./dags/data/house_price_data.csv"

###############################################
# DAG Definition
###############################################
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["pioneer22022001@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
        dag_id="catboost_train_model", 
        description="This DAG runs a model.",
        default_args=default_args, 
        schedule_interval=timedelta(1)
    )

start = DummyOperator(task_id="start", dag=dag)


# spark_job = SparkSubmitOperator(
#     task_id="spark_job_clean_data_1",
#     application="./dags/clean_data.py", # Spark application path created in airflow and spark cluster
#     name="spark_clean_data",
#     conn_id="spark_local",
#     verbose=1,
#     conf={"spark.master":spark_master},
#     # application_args=[csv_file],
#     dag=dag)
train_model = BashOperator(
    task_id='train_model',
    bash_command='python /opt/airflow/dags/catboost/train_model.py',
    dag=dag
)

end = DummyOperator(task_id="end", dag=dag)

start >> train_model >> end