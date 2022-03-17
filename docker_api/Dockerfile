FROM python:3.8
WORKDIR /usr/src/app
COPY matflow ./matflow
COPY requirements.txt .
COPY Pipfile* .
RUN pip install -r requirements.txt
CMD python -m matflow.main