from flask import Flask, request, jsonify
from rejson import Client, Path
import json
from json import dumps
import datetime
from datetime import date, timezone
import time

from influxdb_client import InfluxDBClient, Dialect
from influxdb_client.client.write_api import SYNCHRONOUS



app = Flask(__name__)



def addTimeStamp(jsonData):
      epoch = datetime.datetime.now().timestamp()
      jsonData["timestamp"] = round(epoch)
      return jsonData

def sendToInfluxdb(jsonData):
  with InfluxDBClient(url="http://influxdb:8086", token="mytoken", org="pwr", debug=True) as client:
    with client.write_api(write_options=SYNCHRONOUS) as write_api:
        write_api.write(bucket="grafana", record=jsonData)

def getFromInfluxdb(sensor):
    with InfluxDBClient(url="http://stacyjka.ddns.net:8086", token="mytoken", org="pwr", debug=True) as client:
        query = f'''
            from(bucket: "grafana") 
            |> range(start: -100h ) 
            |> last()
            |> filter(fn: (r) => r._measurement == "{sensor}")
            '''
        query_api = client.query_api()
        csv_result = query_api.query_csv(query,
                                         dialect=Dialect(header=False, delimiter=",", comment_prefix="#",
                                                         annotations=[],
                                                         date_time_format="RFC3339"))
        data = {}
        for csv_line in csv_result:
            if not len(csv_line) == 0:
                # print(f'"{csv_line[7]}":, "{csv_line[6]}"')
                data |= {csv_line[7]: csv_line[6]}
        return data

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":       
        return "Wrong api call"
    else:
        return "Wrong api call"

@app.route("/api/bmp", methods=["POST", "GET"])
def api_bmp():
    if request.method == "POST":
        obj=request.get_json()
        sendToInfluxdb(obj)
        return obj
    else:
        response = getFromInfluxdb("BMP")
        return response

@app.route("/api/pms", methods=["POST", "GET"])
def api_pms():
    if request.method == "POST":
        obj=request.get_json()
        sendToInfluxdb(obj)
        return obj     
    else:
        response = getFromInfluxdb("PMS")
        return response

@app.route("/api/shield", methods=["POST", "GET"])
def api_shield():
    if request.method == "POST":
        obj=request.get_json()
        sendToInfluxdb(obj)
        return obj     
    else:
        response = getFromInfluxdb("SHIELD")
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)