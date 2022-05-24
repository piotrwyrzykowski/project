from flask import Flask, request
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd



app = Flask(__name__)


def sendToInfluxdb(jsonData):
  with InfluxDBClient(url="http://influxdb:8086", token="mytoken", org="pwr", debug=True) as client:
    with client.write_api(write_options=SYNCHRONOUS) as write_api:
        write_api.write(bucket="grafana", record=jsonData)

def getFromInfluxdb(sensor):
    with InfluxDBClient(url="http://influxdb:8086", token="mytoken", org="pwr", debug=True) as client:
        query = f'''
            from(bucket: "grafana") 
            |> range(start: -100h ) 
            |> last()
            |> filter(fn: (r) => r._measurement == "{sensor}")
            |> keep(columns: ["_time", "_field", "_value"])
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") 
            |> yield()
            '''
        df = client.query_api().query_data_frame(query, org="pwr")
        return df.to_json(orient='records').strip("[]")
    

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