import typing as tp
import os

import pandas as pd

FILE_MAP = tp.Dict[str, str]
DF = pd.DataFrame


def lines_to_str(file_as_list: list) -> str:
    """Transform list of lines in one str data"""
    f = str()
    for item in file_as_list:
        f += item
    return f


def read_files(path: str) -> tp.Union[None, FILE_MAP]:
    """Return all files recursively if given a folder.

    It'll return a dictionay with file name as key and the file as string.
    If a file is given, then return only the file as dict.


    :param path: Path for root folder or to file
    :type path: ``str``
    :return: files as `str` on dict with name as key
    :rtype: ``dict``
    """
    if not os.path.exists(path):
        return {path: "error"}

    # was given a file instead a folder
    try:
        folder_items = os.listdir(path)
    except NotADirectoryError:
        # is not a folder
        with open(path) as f:
            file = f.readlines()
            return {path.split("/")[-1]: lines_to_str(file)}

    key = path.split("/")[-1]
    if key == "":
        key = path.split("/")[-2]

    out = {key: dict()}
    for item in folder_items:
        if path[-1] == "/":
            actual_path = path + item
        else:
            actual_path = path + "/" + item
        try:
            item_data = os.listdir(item)
            for data in item_data:
                out[key].update(read_files(data))
        except FileNotFoundError:
            out[key].update(read_files(actual_path))

    return out


def load_dataset(path: str) -> DF:
    path = "./guideToDocuments.csv"
    df = pd.read_csv(path)
    print(df.groupby(["Author"]).size())
    return df