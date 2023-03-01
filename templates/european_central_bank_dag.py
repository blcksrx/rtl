import datetime
import logging

from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator, get_current_context
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

logger = logging.getLogger(__name__)


def load_to_storage():
    context = get_current_context()
    task_instance = context.get("ti")
    filename = f"storage/{task_instance.run_id}_xcom.json"
    logger.info("store task xcom to storage: %s", filename)
    with open(filename, "w", encoding="utf-8") as output_file:
        output_file.write(task_instance.xcom_pull(task_ids="extract_task"))


with DAG(
    dag_id="{{ dag_id }}",
    schedule="{{ schedule }}",
    start_date=datetime.datetime.fromisoformat("{{ start_date }}"),
    end_date=datetime.datetime.fromisoformat("{{ end_date }}"),
    on_failure_callback=EmailOperator(
        to="example@gmail.com",
        subject="error",
        html_content="<h1>error</h1>",
        task_id="error_task",
    ).execute,
    concurrency=1,
    max_active_runs=1,
    dagrun_timeout=datetime.timedelta(seconds=60),
    default_args={"owner": "airflow", "retires": 5, "retry_delay_sec": 300},
) as dag:
    extract_task = SimpleHttpOperator(
        task_id="extract_task",
        method="GET",
        http_conn_id="european_central_bank_api_conn",
        endpoint="{{ extract_task.dataset }}/"
        "{{ extract_task.key }}?"
        "{{ extract_task.params | join('&') }}",
        response_check=lambda response: response.status_code == 200,
        response_filter=lambda response: response.text if response.text else "{}",
        do_xcom_push=True,
    )

    load_storage_task = PythonOperator(
        task_id="load_storage_task", python_callable=load_to_storage
    )

    load_database_task = MySqlOperator(
        task_id="load_database_task",
        mysql_conn_id="{{ load_database_task.load_database_conn }}",
        sql="""
        {{ load_database_task.load_database_sql }}
        """,
    )

    transform_database_task = MySqlOperator(
        task_id="transform_database_task",
        mysql_conn_id="{{ transform_database_task.transform_database_conn }}",
        sql="""
        {{ transform_database_task.transform_database_sql }}
        """,
    )

    extract_task >> load_storage_task
    extract_task >> load_database_task
    load_database_task >> transform_database_task
