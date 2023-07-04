from dotenv import load_dotenv
from os import getenv
from enum import Enum

# Load environment variables from .env file
load_dotenv()

class Config:
    def __init__(self, testing=None, log_directory=None):
        self.TESTING = testing if testing is not None else (getenv('TESTING', 'False') == 'True')
        self.LOG_DIRECTORY = log_directory if log_directory is not None else ('tests/log/' if self.TESTING else '/var/log/')


class ErrorMessage(Enum):
    INVALID_FILENAME = 'Invalid filename: must not contain ".." or start with "/"'
    LONG_SEARCH_TERM = "Search term is too long: must be 100 characters or fewer"
    INVALID_LIMIT = "Invalid limit value: must be between 1 and 1000"
