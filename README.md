# FlaskLogMonitor

This project offers a solution for on-demand log monitoring across multiple unix-based servers. With this service, it is no longer necessary to individually access each server and manually open the log files located at /var/log. Instead, by sending a simple REST request to a server, you can easily retrieve its /var/log files. This makes tracking and debugging system events considerably more efficient and user-friendly.

## Installation and Setup

1. Install Python 3.9.
2. Install the dependencies by running `pip install -r requirements.txt`.
3. Run the server by using `python app.py`.


## Running the Tests

Run the tests with the following command:

```bash
python -m unittest tests
```

## Contributing

Please open an issue to discuss potential contributions before submitting a pull request.

## License

This project is licensed under the terms of the MIT license.

