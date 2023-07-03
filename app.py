from flask import Flask, jsonify, request, Response
from views.log_view import get_logs
from views.home_view import home


def create_app(test_config=None):
    app = Flask(__name__)

    # Add routes
    app.add_url_rule("/", view_func=home, methods=["GET"])
    app.add_url_rule("/logs", view_func=get_logs, methods=["GET"])

    # override configuration if test_config is provided
    if test_config is not None:
        app.config.from_mapping(test_config)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
