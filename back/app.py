from flask import Flask, request, jsonify
from rejson import Client, Path
import psycopg2
import json

app = Flask(__name__)

rj = Client(host='redis', port=6379, decode_responses=True)

conn = psycopg2.connect(
    host="db",
    database="python_data",
    user="postgres",
    password="example")
TABLE_NAME = "data"

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        obj=request.get_json()
        rj.jsonset('obj', Path.rootPath(), obj)
        #cur = conn.cursor()
        print(obj)

        return "response"
    else:
        response = rj.jsonget('obj',Path('.sensor'))
        #response = rj.jsonget('obj')
        #cur = conn.cursor()
        #
        # cur.execute("select * from %s where name = 'BMP'"),TABLE_NAME
        #foo = json.dumps(cur.fetchall())
        #cur.close()
        #print(foo)
        return response
@app.route("/redis/bmp", methods=["POST", "GET"])
def redis_bmp():
    if request.method == "POST":
        obj=request.get_json()
        rj.jsonset('bmp', Path.rootPath(), obj)
        print(obj)
        return "bmp to redis"
    else:
        response = rj.jsonget('bmp',Path.rootPath())
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
