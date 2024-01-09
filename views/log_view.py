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
    """
    Retrieve log entries from a specified log file.

    This function extracts log entries from a file in the log directory. The log file, search term, and limit on the number of lines returned can be specified via request arguments. The function validates the filename, search term, and lines limit, and returns appropriate HTTP status codes and messages in case of any invalid inputs.

    The function operates as follows:
    - Extracts the log directory path from the application configuration.
    - Retrieves the filename, search term, and lines limit from request arguments with default values for each.
    - Validates the filename, search term, and lines limit, returning a 400 BAD REQUEST status with an error message if any validation fails.
    - Checks if the specified file exists in the log directory, returning a 404 NOT FOUND status with an error message if it does not.
    - Reads the specified number of lines from the file, optionally filtering by the search term.
    - Returns the log lines in a JSON response with a 200 OK status if successful.

    Returns:
        A tuple containing a Flask `Response` object with the log data or error message in JSON format, and an `HTTPStatus` code indicating the result of the operation.

    Raises:
        The function can implicitly raise exceptions related to file access or JSON operations but does not explicitly raise any exceptions itself.
    """
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
