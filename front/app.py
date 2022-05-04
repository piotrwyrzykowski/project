from flask import Flask, render_template, request
import requests
import sys

import datetime
from datetime import date, timezone
import pytz



app = Flask(__name__)

backend_URL = "http://backend:5001"
ip = "graph"
def get_redis_bmp():
    return requests.get(url=backend_URL+"/api/bmp").json()


def get_redis_pms():
    return requests.get(url=backend_URL+"/api/pms").json()

@app.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html", data_bmp=get_redis_bmp(), data_pms=get_redis_pms(), ip=ip)

@app.route("/graph", methods=["POST","GET"])
def graph():
    ulll = 'http://stacyjka.ddns.net:3000/d/oT0yskU7z/new-dashboard?orgId=1&viewPanel=2'
    return render_template("graphs.html", url=ulll)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
