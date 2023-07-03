from re import search


def is_filename_valid(filename: str):
    """
    Check if the filename does not contain path traversal sequences
    and does not start with '/'
    """
    if ".." not in filename and not filename.startswith("/"):
        return True
    return False


def is_search_term_valid(search_term):
    """Check if the search term is not too long"""
    return len(search_term) <= 100


def is_limit_valid(limit):
    """Check if the number of lines to return is within a valid range"""
    return 1 <= limit <= 1000


def get_file_lines(filepath, search_term, num_lines_to_return):
    """
    Read the file, filter lines based on the search term,
    and return the last num_lines_to_return lines
    """
    with open(filepath, "r") as f:
        lines = f.readlines()

    if search_term:
        lines = [line for line in lines if search(search_term, line)]

    return lines[-num_lines_to_return:]
