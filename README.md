## How to run pipeline
1. Ensure that your Docker Desktop is running.
2. Open your IDE, install Docker and Python plugin/extension if necessary (I'm using VS Code).
3. Build docker image from dockerfile (my image is hao_airflow:latest).
4. Modify the service name and image name in the docker-compose.yml file, then compose up.
5. Navigate to http://localhost:8080/ in your web browser, and use the following credentials to log in: Username: admin, Password: the password can be found in the standalone_admin_password.txt file. After logging in, you should have access to the Airflow UI.
6. Go back to your IDE, where you should observe that the airflow folder has been created. Within this airflow folder, create a new folder named "dags".
7. Copy or clone the "ingests_reddit.py" file from GitHub and paste it into the "dags" folder that you created within the "airflow" folder. Save the file in this location.
8. Return to the Airflow UI and wait a few minutes until the DAG named "ingests_reddit" appears.
9. In the top sidebar, navigate to Admin -> Connections. Click on the "+" button to add a new record.
10. Put "mongo_conn_id" as the connection ID and select "MongoDB" as the connection type. Fill in the Host, Login, and Password fields with the respective information for your MongoDB service. In the Extra field (last one), enter "{"srv": true}".
11. Replace the database name and collection name in the "ingests_reddit.py" file on lines 47 and 48 with your own.
12. In the Airflow UI, navigate back to the DAGs section and select the "ingests_reddit" DAG. Then, click on the "Trigger DAG" button located on the right side to trigger the job.
13. After the job successfully completes, you can proceed to query the data in your MongoDB collection.

## Assumption & Explanation
1. I used MongoDB Atlas to set up a local MongoDB instance. Additionally, I'm doing some research on deploying an instance via Docker and learning how to use the MongoDB Shell.
2. This pipeline runs weekly, with the schedule_interval set for 12 PM every Sunday. It can be adjusted to run at any desired cadence.
3. The downloadable URL for this pipeline is currently hardcoded. Ideally, it should be dynamically generated, especially if the URL contains a timestamp.
4. The only transformation I performed was flattening the nested JSON structure. As I gain a deeper understanding of how the data is utilized, I expect to generate more ideas for additional transformations.
5. The only test I implemented was to ensure DAG integrity. To develop the data quality module further, I require additional sample data. However, in case of job failure, Airflow logs will provide sufficient information for debugging purposes.
6. Please find the execution result enclosed in the screenshots.
