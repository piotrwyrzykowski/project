from flask import Flask, request, jsonify

app = Flask(__name__)

database = [{'sensor':'piotr','temp':'22'}]


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        database.append(request.get_json())
        return "response"
    else:
        response = jsonify(database)

        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
