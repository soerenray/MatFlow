FROM python:3.8

COPY ./ $HOME/matflow_data/
RUN (cd /matflow_data/ && pip install -r requirements.txt)

FROM node:12.18.1
COPY ./ $HOME/matflow_data/
RUN (cd /matflow_data/ && npm install)
CMD (cd /matflow_data/ && npm run serve -- --port 8081)


