FROM apache/airflow:2.2.3-python3.8
RUN pip install --no-cache-dir apache-airflow-providers-docker==2.1.0
RUN pip install --no-cache-dir Flask
RUN airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
USER airflow
