from flask import Flask, request, jsonify
from rejson import Client, Path
import json
from json import dumps
import jsonschema
from jsonschema import validate
import datetime
from datetime import date, timezone
import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS



app = Flask(__name__)

rj = Client(host='redis', port=6379, decode_responses=True)


bmpSchema = {
  "type": "object",
  "properties": {
    "name": { "enum": ["BMP", "PMS"] },
    "temp": { "type": "number" },
    "hum": { "type": "number" },
    "press": { "type": "number" },
    "pm1.0": { "type": "number" },
    "pm2.5": { "type": "number" },
    "pm10": { "type": "number" }
  },
  "allOf":[
    { 
      "if": {
        "properties": { "name": { "const": "BMP" }},
        "required": ["name"]
      },
      "then": {
        "required": ["temp","hum","press"]
        }
    },
    {
      "if":{
        "properties": { "name": { "const": "PMS" }},
        "required": ["name"]
      },
      "then": {
        "required": ["pm1_0","pm2_5","pm10"]
        }
    }
  ]
}

def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=(bmpSchema))
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

def addTimeStamp(jsonData):
      epoch = datetime.datetime.now().timestamp()
      jsonData["timestamp"] = round(epoch)
      return jsonData

def sendToRedis(jsonData):
  data = jsonData['name']
  rj.jsonset( data, Path.rootPath(), addTimeStamp(jsonData))

def sendToInfluxdb(jsonData):
  with InfluxDBClient(url="http://influxdb:8086", token="mytoken", org="pwr", debug=True) as client:
    with client.write_api(write_options=SYNCHRONOUS) as write_api:
        loaded = json.loads( '{"measurement": "BMP", "fields":{"temp": 234, "hum": 20, "press": 1021}}')
        #loaded = json.loads( '{"measurement": "Messungen", "tags": {"Ort": "Rxxxx"}, "fields": {"temp1": 2.6, "hum1": 66.0, "temp2": 2.3, "hum2": 81.0, "temp3": 22.0, "hum3": 32.0}}')

        write_api.write(bucket="bar", record=loaded)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":       
        return "Wrong api call"
    else:
        return "Wrong api call"

@app.route("/redis/bmp", methods=["POST", "GET"])
def redis_bmp():
    if request.method == "POST":
        obj=request.get_json()
        isValid = validateJson(obj)
        if isValid:
            sendToRedis(obj)
            sendToInfluxdb(obj)
            return "valid json data"
        else:
            return "json is invalid"       
    else:
        response = rj.jsonget('BMP',Path.rootPath())
        return response

@app.route("/redis/pms", methods=["POST", "GET"])
def redis_pms():
    if request.method == "POST":
        obj=request.get_json()
        isValid = validateJson(obj)
        if isValid:
            sendToRedis(obj)
            sendToInfluxdb(obj)
            return "valid json data"
        else:
            return "json is invalid"       
    else:
        response = rj.jsonget('PMS',Path.rootPath())
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)