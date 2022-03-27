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
    "hum": {
      "type": "number"
    },
    "name": {
      "type": "string"
    },
    "press": {
      "type": "number"
    },
    "temp": {
      "type": "number"
    }
  },
  "required": [
    "hum",
    "name",
    "press",
    "temp"
  ]
}
def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=bmpSchema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

def addTimeStamp(jsonData):
      epoch = datetime.datetime.now().timestamp()
      #epoch = epoch.replace(tzinfo=timezone.utc)
      jsonData["timestamp"] = round(epoch)
      return jsonData

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
            rj.jsonset('bmp', Path.rootPath(), addTimeStamp(obj))
            return "valid json data"
        else:
            return "json is invalid"       
    else:
        response = rj.jsonget('bmp',Path.rootPath())
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
