from dotenv import load_dotenv
from os import getenv
from enum import Enum

# Load environment variables from .env file
load_dotenv()
IS_LOCAL = getenv("IS_LOCAL", "False") == "True"
LOG_DIRECTORY = "tests/var/log/" if IS_LOCAL else "/var/log/"


class ErrorMessage(Enum):
    INVALID_FILENAME = 'Invalid filename: must not contain ".." or start with "/"'
    LONG_SEARCH_TERM = "Search term is too long: must be 100 characters or fewer"
    INVALID_LIMIT = "Invalid limit value: must be between 1 and 1000"
