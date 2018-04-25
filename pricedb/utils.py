""" Various utilities """
from typing import List


def split_symbol(symbol: str) -> (str, str):
    """ Splits the symbol into namespace, symbol tuple """
    symbol_parts = symbol.split(":")
    namespace = None
    mnemonic = symbol

    if len(symbol_parts) > 1:
        namespace = symbol_parts[0]
        mnemonic = symbol_parts[1]

    return namespace, mnemonic


def read_lines_from_file(file_path: str) -> List[str]:
    """ Read text lines from a file """
    # check if the file exists?
    with open(file_path) as csv_file:
        content = csv_file.readlines()
    return content
