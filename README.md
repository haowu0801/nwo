## How to run pipeline
1. Makesure your docker desktop is running.
2. Open your IDE, install Docker and Python plugin/extension if necessary (I'm using VS Code).
3. Build docker image from dockerfile (my image is hao_airflow:latest).
4. Update the service name and image name in docker-compose.yml, then compose up.
5. Visit http://localhost:8080/ and enter creds (username is admin, pass in standalone_admin_password.txt), then you should have accees to the Airflow UI.
6. Return to your IDE, you should find the airflow folder is created. Create a new folder with name dags inside the airflow folder.
7. Copy/clone the ingests_reddit.py from github and paste it under dags folder, save the file.
8. Back to Airflow UI, wait few mins till dag ingests_reddit shows up.
9. On the top sidebar, click Admin -> Connections, then click "+" button to add a new record.
10. Put "mongo_conn_id" as connection id and select MongoDB as connection type, then fill the Host, Login and Password of your MongoDB service. Put "{"srv": true}" in the Extra field (last one)
11. Replace DB name and collection name in ingests_reddit.py line 47 & 48 with yours.
12. In Airflow UI, back to DAGs and select ingests_reddit, click the Trigger DAG button on the right.
13. Once the job succeed, you can query the data in your collection.

## Assumption & Explanation
1. I used 1. I used MongoDB Atlas MongoDB Atlas to set up a local MongoDB instance. Additionally, I'm doing some research on deploying an instance via Docker and learning how to use the MongoDB Shell.
2. This pipeline runs weekly, with the schedule_interval set for 12 PM every Sunday. It can be adjusted to run at any desired cadence.
3. The downloadable URL for this pipeline is currently hardcoded. Ideally, it should be dynamically generated, especially if the URL contains a timestamp.
4. The only transformation I performed was flattening the nested JSON structure. As I gain a deeper understanding of how the data is utilized, I expect to generate more ideas for additional transformations.
5. The only test I implemented was to ensure DAG integrity. To develop the data quality module further, I require additional sample data.
6. Please find the execution report enclosed in the screenshots.
