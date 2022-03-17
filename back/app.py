from flask import Flask, request, jsonify

app = Flask(__name__)

database = []


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        animal = request.form["sensor"]
        name = request.form["temp"]

        database.append({"sensor": name, "temp": animal})

        return f"[BACKEND] Name: {name} Animal: {animal} added to the database"

    else:
        response = jsonify(database)

        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
