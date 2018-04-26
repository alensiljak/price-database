""" Various utilities """
from typing import List


def read_lines_from_file(file_path: str) -> List[str]:
    """ Read text lines from a file """
    # check if the file exists?
    with open(file_path) as csv_file:
        content = csv_file.readlines()
    return content
