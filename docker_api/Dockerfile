FROM python:3.8
COPY ./ $HOME/matflow_data/
RUN (cd /matflow_data/ && pip install -r requirements.txt)
CMD (cd /matflow_data/ && python -m matflow.main)