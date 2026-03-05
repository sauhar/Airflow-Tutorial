from airflow.sdk import dag, task, asset
from pendulum import datetime
import os
from asset_13 import fetch_assets_data #import qst asset

@asset(
    schedule=fetch_assets_data, #take data from the fetch_assets_data asset and use it as a schedule for this asset
     # This is optional but good to include, it says where our assest is pointing to and what is the name of the assest
    uri="/opt/airflow/logs/data/data_processed.txt",
    name="process_data"
)
def process_data(self):

    # Ensure the directory exists
    os.makedirs(os.path.dirname(self.uri), exist_ok=True)

    # Simulate data processing by writing to a file
    with open(self.uri, 'w') as f:
        f.write(f"Data processed successfully")

    print(f"Data processed to {self.uri}")