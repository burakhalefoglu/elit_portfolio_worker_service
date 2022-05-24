import os

import pandas as pd


def get_resources_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_resources_by_file_name(file: str) -> pd.DataFrame:
    """

    :param file: str:
    :return:
    :example: "stocks.csv"
    """
    resource_path = get_resources_path() + "\\" + file
    stocks = pd.read_csv(
        resource_path,
        keep_default_na=False,
    )
    return stocks
