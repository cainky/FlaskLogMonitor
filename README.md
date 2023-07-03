# FlaskLogMonitor

This project offers a solution for on-demand log monitoring across multiple unix-based servers. With this service, it is no longer necessary to individually access each server and manually open the log files located at /var/log. Instead, by sending a simple REST request to a server, you can easily retrieve its /var/log files. This makes tracking and debugging system events considerably more efficient and user-friendly.

## Installation and Setup

1. Install Python 3.10.6
2. [Install Poetry](https://python-poetry.org/docs/#installation) - Poetry is used for dependency management.

```bash
curl -sSL https://install.python-poetry.org | python -
```
3. Install the project dependencies
```bash
poetry install
```

4. Run the server
```bash
poetry run python app.py
```


## Running the Tests

```bash
poetry run python -m unittest discover
```

## Contributing

Please open an issue to discuss potential contributions before submitting a pull request.

## License

This project is licensed under the terms of the MIT license.

