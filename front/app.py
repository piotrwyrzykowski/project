from flask import Flask, render_template, request
import requests
import sys



app = Flask(__name__)

backend_URL = "http://backend:5001"
ip = "pms"
def get_redis_bmp():
    return requests.get(url=backend_URL+"/api/bmp").json()

def get_redis_pms():
    return requests.get(url=backend_URL+"/api/pms").json()


@app.route("/", methods=["POST","GET"])
def index():
    ulll='http://192.168.1.240:3000/d-solo/oT0yskU7z/new-dashboard?orgId=1&panelId=2"'
    return render_template("index.html", data_bmp=get_redis_bmp(), data_pms=get_redis_pms(), ip=ip)

@app.route("/pms", methods=["POST","GET"])
def pms():
    ulll='http://192.168.1.240:3000/d-solo/oT0yskU7z/new-dashboard?orgId=1&panelId=2"'
    return render_template("graphs.html", data_bmp=get_redis_bmp(), data_pms=get_redis_pms(), url=ulll)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
