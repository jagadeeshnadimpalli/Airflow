from airflow.sdk import dag, task


@dag
def sql_decorator_dag():

    @task.sql(
        conn_id="postgres"
    )
    def sql_command():
        return "select count(*) from xcom" #airflow databses
    
    sql_command()

sql_decorator_dag()


