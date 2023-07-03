# FlaskLogMonitor

This project provides on-demand monitoring of various unix-based servers without having to log into each individual machine and opening up the log files found in `/var/log`. You can issue a REST request to a machine to retrieve logs from `/var/log` on the machine receiving the REST request.

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

