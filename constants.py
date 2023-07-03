from enum import Enum


class ErrorMessage(Enum):
    INVALID_FILENAME = 'Invalid filename: must not contain ".." or start with "/"'
    LONG_SEARCH_TERM = "Search term is too long: must be 100 characters or fewer"
    INVALID_LIMIT = "Invalid limit value: must be between 1 and 1000"
