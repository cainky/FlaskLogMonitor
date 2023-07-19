from flask import jsonify, request, Response
from os import path
from http import HTTPStatus

from constants import ErrorMessage
from app_utils import (
    get_file_lines,
    is_filename_valid,
    is_limit_valid,
    is_search_term_valid,
)
from flask import current_app as app

from werkzeug.utils import secure_filename

def get_logs() -> tuple[Response, HTTPStatus]:
    log_directory = app.config["LOG_DIRECTORY"]
    filename = request.args.get("filename", default="syslog", type=str)
    search_term = request.args.get("term", default="", type=str)
    lines_limit = request.args.get("limit", default=50, type=int)
    
    if not is_filename_valid(filename):
        return (
            jsonify(error=ErrorMessage.INVALID_FILENAME.value),
            HTTPStatus.BAD_REQUEST,
        )
    filename = secure_filename(filename)

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

    filepath = log_directory + filename
    if not path.isfile(filepath):
        return (
            jsonify(error=f"File not found: {log_directory}{filename} does not exist"),
            HTTPStatus.NOT_FOUND,
        )

    lines = get_file_lines(filepath, search_term, lines_limit)

    return jsonify(lines=lines), HTTPStatus.OK
