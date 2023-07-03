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
Alternatively you can use ```poetry shell``` to activate the environment and run python commands as you normally would: ```python app.py```


## Project Files and Directories
```
.
├── .env                # Environment variables
├── README.md           # This file
├── app.py              # The main application script
├── views               # Request & response handling
└── tests               # Tests for the app
    └── var
        └── log         # Directory for local testing of logs
```
#### `.env`
Be sure to create this file for local testing and development.
This file contains environment variables for local development. It is read by `dotenv.load_dotenv()` at the start of `app.py`. 

The environment variables are:

- `IS_LOCAL`: Determines whether the app is running in a local development environment. If `True`, the app will read from the local `tests/var/log` directory for log files. If `False` or not set, the app will read from `/var/log`.

#### `README.md`

This file provides information about the project, including this description of the file structure.

#### `app.py`

This is the main script for the Flask application. It defines the route for the log reading API and handles requests to that route. The log reading functionality is controlled by environment variables.

#### `tests/var/log`

This directory is used for local testing of the log reading functionality. When `IS_LOCAL` is `True`, the app will attempt to read log files from this directory. You can place any files you want to test with in this directory.

## Running the Tests

```bash
poetry run python -m unittest
```

## Contributing

Please open an issue to discuss potential contributions before submitting a pull request.

## License

This project is licensed under the terms of the MIT license.

