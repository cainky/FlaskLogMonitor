from flask import Flask, jsonify, request
import os
from http import HTTPStatus
from constants import ErrorMessage
from app_utils import (
    get_file_lines,
    is_filename_valid,
    is_limit_valid,
    is_search_term_valid,
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
IS_LOCAL = os.getenv("IS_LOCAL", "False") == "True"
LOG_DIRECTORY = "tests/var/log/" if IS_LOCAL else "/var/log/"


app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello, World!"


@app.route("/logs", methods=["GET"])
def get_logs():
    filename = request.args.get("filename", default="syslog", type=str)
    search_term = request.args.get("term", default="", type=str)
    lines_limit = request.args.get("limit", default=50, type=int)

    if not is_filename_valid(filename):
        return (
            jsonify(error=ErrorMessage.INVALID_FILENAME.value),
            HTTPStatus.BAD_REQUEST,
        )
    if not is_search_term_valid(search_term):
        return (
            jsonify(error=ErrorMessage.LONG_SEARCH_TERM.value),
            HTTPStatus.BAD_REQUEST,
        )
    if not is_limit_valid(lines_limit):
        return (
            jsonify(error=ErrorMessage.INVALID_LIMIT.value),
            HTTPStatus.BAD_REQUEST,
        )

    filepath = LOG_DIRECTORY + filename
    if not os.path.isfile(filepath):
        return (
            jsonify(error=f"File not found: {LOG_DIRECTORY}{filename} does not exist"),
            HTTPStatus.NOT_FOUND,
        )

    lines = get_file_lines(filepath, search_term, lines_limit)

    return jsonify(lines=lines), HTTPStatus.OK


if __name__ == "__main__":
    app.run(debug=True)
