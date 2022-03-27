from flask import Flask, render_template, request
import requests
import sys



app = Flask(__name__)

backend_URL = "http://backend:5001"

def get_redis_bmp():
    return requests.get(url=backend_URL+"/redis/bmp").json()


@app.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html", data_bmp=get_redis_bmp())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
