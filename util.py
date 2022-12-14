import os

import requests

headers = {
    "cookie": os.environ.get("AOC_COOKIE"),
}


def read_data(day: int) -> str:
    url = f"https://adventofcode.com/2022/day/{day}/input"
    response = requests.get(url, headers=headers)
    return response.text
