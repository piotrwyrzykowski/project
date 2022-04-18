from flask import Flask, request, jsonify
from rejson import Client, Path
import json
from json import dumps
import datetime
from datetime import date, timezone
import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS



app = Flask(__name__)

rj = Client(host='redis', port=6379, decode_responses=True)



def addTimeStamp(jsonData):
      epoch = datetime.datetime.now().timestamp()
      jsonData["timestamp"] = round(epoch)
      return jsonData

def sendToRedis(jsonData):
  data = jsonData['measurement']
  rj.jsonset( data, Path.rootPath(), addTimeStamp(jsonData))

def sendToInfluxdb(jsonData):
  with InfluxDBClient(url="http://influxdb:8086", token="mytoken", org="pwr", debug=True) as client:
    with client.write_api(write_options=SYNCHRONOUS) as write_api:
        write_api.write(bucket="grafana", record=jsonData)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":       
        return "Wrong api call"
    else:
        return "Wrong api call"

@app.route("/api/bmp", methods=["POST", "GET"])
def redis_bmp():
    if request.method == "POST":
        obj=request.get_json()
        sendToRedis(obj)
        sendToInfluxdb(obj)
        return obj
    else:
        response = rj.jsonget('BMP',Path.rootPath())
        return response

@app.route("/api/pms", methods=["POST", "GET"])
def redis_pms():
    if request.method == "POST":
        obj=request.get_json()
        sendToRedis(obj)
        sendToInfluxdb(obj)
        return obj     
    else:
        response = rj.jsonget('PMS',Path.rootPath())
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)