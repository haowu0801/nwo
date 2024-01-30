from datetime import datetime, timedelta
from flatten_json import flatten
import gdown
import io
import json
import jsonlines
import zstandard

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.exceptions import AirflowException
from airflow.utils.dates import days_ago

def prior_week_end():
    return (datetime.now() - timedelta(days=((datetime.now().isoweekday()) % 7))).strftime("%Y-%m-%d")

def etl():
    # download latest file
    url = 'https://drive.google.com/file/d/1E7iRwCp7IjvCjh_-owrt2NTMWnvgleZp/view'
    download = str(prior_week_end())+'.zst'
    gdown.download(url, download, quiet=True, fuzzy=True)
    print("Downloading file " + download)

    with open(download, "rb") as f:
        dctx = zstandard.ZstdDecompressor(max_window_size=2147483648)
        stream_reader = dctx.stream_reader(f)
        text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')
        output = list()
        for line in text_stream:
            obj = json.loads(line)
            output.append(obj)

    # flatten nested json data
    output_flattend = [flatten(item) for item in output]

    # save to json lines
    saved_file=str(prior_week_end())+'.jsonl'
    with jsonlines.open(saved_file, "w") as writer:
        writer.write_all(output_flattend)

    # upload raw data to MongoDB
    try:
        hook = MongoHook(mongo_conn_id='mongo_conn_id')
        client = hook.get_conn()
        # replace below with your db name and collection name
        db = client.haoDB
        collection=db.haoCollection
        print(f"Connected to MongoDB - {client.server_info()}")
        collection.insert_many(output_flattend)
        print(f"Inserted {len(output_flattend)} records")
    except Exception as e:
        print(f"Error connecting to MongoDB -- {e}")
        raise AirflowException

dag = DAG(
    dag_id="ingests_reddit",
    start_date=days_ago(1),
    schedule_interval='0 12 7 * *',
    default_args={
        "owner": "nwo",
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    },
    description="Ingests Reddit posts and comments and associated metadata from relevant subreddits"
)

ingests_reddit = PythonOperator(
    task_id='ingests_reddit',
    python_callable=etl,
    dag=dag
)

ingests_reddit
