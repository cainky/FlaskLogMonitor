from flask import Request
from typing import List, Tuple
from os import SEEK_END

from typing.io import IO


def get_request_params(request: Request) -> Tuple[str, str, int]:
    filename = request.args.get("filename", default="syslog", type=str)
    search_term = request.args.get("term", default="", type=str)
    lines_limit = request.args.get("limit", default=50, type=int)

    return filename, search_term, lines_limit


def is_filename_valid(filename: str) -> bool:
    """
    Validates a filename for path traversal and absolute paths.

    The filename is considered valid if it does not contain any ".." (used for path traversal)
    and does not start with "/" (indicating an absolute path).

    Args:
        filename (str): The filename to be checked.

    Returns:
        bool: True if filename is valid, False otherwise.
    """
    return ".." not in filename and not filename.startswith("/")


def is_search_term_valid(search_term: str) -> bool:
    """
    Validates a search term based on its length.

    The search term is considered valid if its length is less than or equal to 100.

    Args:
        search_term (str): The search term to be checked.

    Returns:
        bool: True if search term is valid, False otherwise.
    """
    return len(search_term) <= 100


def is_limit_valid(limit: int) -> bool:
    """
    Validates a limit for the number of lines to return.

    The limit is considered valid if it's within the range 1 to 1000, inclusive.

    Args:
        limit (int): The limit to be checked.

    Returns:
        bool: True if limit is valid, False otherwise.
    """
    return 1 <= limit <= 1000


def get_file_lines(
    filepath: str, search_term: str, num_lines_to_return: int
) -> List[str]:
    """
    Retrieves a specified number of lines from a file,
    optionally filtering for a search term.

    Args:
        filepath (str): Path to the file.
        num_lines_to_return (int): Number of lines to retrieve from the end of the file.
        search_term (str, optional): Term to filter lines. If None, no filtering is applied.

    Returns:
        List[str]: List of lines from the file.
    """
    lines = tail(filepath, num_lines_to_return)

    if search_term is not None:
        lines = [line for line in lines if search_term in line]

    return lines


def tail(filename: str, lines_limit: int = 50, block_size: int = 1024) -> List[str]:
    """
    Reads a file in reverse and returns its last 'lines_limit' lines.

    Args:
        filename (str): The path to the file to be read.
        lines_limit (int, optional): The maximum number of lines to be returned. Defaults to 50.
        block_size (int, optional): The number of bytes to read at a time. Defaults to 1024.

    Returns:
        List[str]: A list of the last 'lines_limit' lines in the file, in reverse order.
    """

    lines = []
    with open(filename, "r") as f:
        # Seek to the end of the file.
        f.seek(0, SEEK_END)
        # Get the current position in the file.
        block_end_byte = f.tell()

        # Continue reading blocks and adding lines until we have enough lines or reach the start of the file.
        while len(lines) < lines_limit and block_end_byte > 0:
            # Read a block from the file, update the block_end_byte position, and get the new lines.
            new_lines, block_end_byte = read_block(f, block_end_byte, block_size)
            lines.extend(new_lines)

        # Return the last 'lines_limit' lines
        return lines[-lines_limit:]


def read_block(
    file: IO, block_end_byte: int, block_size: int
) -> Tuple[List[str], int]:
    """
    Reads a block from the end of a file and returns the lines in the block.

    Args:
        file (object): The file object to read from.
        block_end_byte (int): The current position in the file.
        block_size (int): The number of bytes to read at a time.

    Returns:
        Tuple[List[str], int]: A tuple containing the list of lines in the block,
                               and the updated position in the file.
    """
    # This is the current position in the file.
    # Use min() to ensure we only step back as far as we can (start of file)
    stepback = min(block_size, block_end_byte)

    # Step back and read a block from the file
    file.seek(block_end_byte - stepback)
    block = file.read(stepback)
    block_end_byte -= stepback
    lines = block.split("\n")

    return lines, block_end_byte
