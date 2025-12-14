from airflow.sdk import asset, Asset, Context
import requests

@asset(
    schedule="@daily",
    uri = "https://randomuser.me/api"
)
def user_asset(self) -> dict[str]:
    response = requests.get(self.uri)
    return response.json()

@asset(
        schedule=user_asset
)
def user_location(user_asset:Asset, context:Context)->dict[str]:
    user_data = context['ti'].xcom_pull(
        dag_id=user_asset.name,
        task_ids=user_asset.name,
        key="return_value",
        include_prior_dates=True #to fetech the latest xcom value we use this parameter
    )
# Debugging print to confirm we got it
    print(f"DEBUG: Pulled data from DAG '{user_asset.name}': {user_data}")
    return user_data['results'][0]['location']

@asset(
    schedule = user_asset
)
def user_login(user_asset:Asset, context:Context):
    user_login_data = context['ti'].xcom_pull(
        dag_id=user_asset.name,
        task_ids=user_asset.name,
        include_prior_dates=True
    )
    # Debugging print to confirm we got it
    print(f"DEBUG: Pulled data from DAG '{user_asset.name}': {user_login_data}")
    return user_login_data['results'][0]['login']

@asset.multi(
          schedule=user_asset,
          outlets=[Asset(name='user_timezone'),
          Asset(name='user_dob')
          ]
)
def user_info(user_asset:Asset, context:Context)->list[dict[str]]:
        user_time_dob = context['ti'].xcom_pull(
        dag_id=user_asset.name,
        task_ids=user_asset.name,
        include_prior_dates=True #to fetech the latest xcom value we use this parameter
        )
        return [
             user_time_dob['results'][0]['location']['timezone'],
             user_time_dob['results'][0]['dob']
        ]
        


