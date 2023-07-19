from flask import Flask
from views.log_view import get_logs
from views.home_view import home
from constants import Config


def create_app(test_config=None):
    app = Flask(__name__)

    # override configuration if test_config is provided
    if test_config is not None:
        app.config.from_mapping(test_config)
    else:
        config = Config(testing=False)
        app.config.from_object(config)

    # Add routes
    app.add_url_rule("/", view_func=home, methods=["GET"])
    app.add_url_rule("/logs", view_func=get_logs, methods=["GET"])

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
