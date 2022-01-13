from __future__ import annotations
from flask import Flask
from flask_restful import Resource, Api
from waitress import serve





        #serve(self.__app, host="127.0.0.1", port=5001)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/get_server_details")
def get_server_details():
    return "boo boo", 607

app.run(debug='true')

