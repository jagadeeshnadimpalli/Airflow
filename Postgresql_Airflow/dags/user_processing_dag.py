from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import requests
from datetime import datetime


@dag
def user_processing():
    create_table = SQLExecuteQueryOperator(
        task_id="Creating_Table",
        conn_id="postgres",
        sql="""CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            email VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
    )

    @task.sensor(poke_interval=30, timeout=300)
    def is_api_available() -> PokeReturnValue:
        response = requests.get(
            "https://raw.githubusercontent.com/marclamberti/datasets/refs/heads/main/fakeuser.json"
        )
        print(response.status_code)
        if response.status_code == 200:
            condition = True
            fake_user = response.json()
        else:
            condition = False
            fake_user = None
        return PokeReturnValue(is_done=condition, xcom_value=fake_user)

    @task
    def extract_user(fake_user):
        return {
            "id": fake_user["id"],
            "first_name": fake_user["personalInfo"]["firstName"],
            "last_name": fake_user["personalInfo"]["lastName"],
            "email": fake_user["personalInfo"]["email"],
        }

    @task
    def process_user(user_info):
        user_info["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = pd.DataFrame([user_info])
        df.to_csv("/tmp/user_info.csv", header=True, index=False)

    @task
    def store_user():
        hook = PostgresHook(postgres_conn_id="postgres")
        hook.copy_expert(
            sql="COPY users FROM STDIN WITH CSV HEADER", filename="/tmp/user_info.csv"
        )

    # dependencies
    process_user(extract_user(create_table >> is_api_available())) >> store_user()


user_processing()  # we must call this otherwise it wont show up in the airflow UI
