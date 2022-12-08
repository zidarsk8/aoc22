import pytest

import util

FULL_TEXT = util.read_data(2)


def get_code(text):
    return int(text)


@pytest.mark.parametrize(
    "text,result",
    [
        ("3", 3),
        ("13", 13),
    ],
)
def test_result(text, result):
    assert get_code(text) == result


def test_dummy():
    assert get_code("135") == 135
