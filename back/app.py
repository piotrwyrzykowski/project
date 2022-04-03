from flask import Flask, request, jsonify
from rejson import Client, Path
import json
from json import dumps
import jsonschema
from jsonschema import validate
import datetime
from datetime import date, timezone
import time

app = Flask(__name__)

rj = Client(host='redis', port=6379, decode_responses=True)


bmpSchema = {
  "type": "object",
  "properties": {
    "name": { "type": "string" },
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
        "required": ["pm1.0","pm2.5","pm10"]
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
            #rj.jsonset('bmp', Path.rootPath(), addTimeStamp(obj))
            return "valid json data"
        else:
            return "json is invalid"       
    else:
        response = rj.jsonget('BMP',Path.rootPath())
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
