FROM apache/airflow:latest

USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

USER airflow

RUN pip install flatten_json
RUN pip install gdown
RUN pip install jsonlines
RUN pip install zstandard
RUN pip install apache-airflow-providers-mongo