from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello, World!"


@app.route("/logs", methods=["GET"])
def get_logs():
    filename = "syslog"
    filepath = "var/log/" + filename
    if not os.path.isfile(filepath):
        return "File not found", 404

    with open(filepath, "r") as f:
        lines = f.readlines()

    return jsonify(lines)


if __name__ == "__main__":
    app.run(debug=True)
