from textwrap import dedent

import pytest

import util

input_text = util.read_data(10)


short_example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


from icecream import ic


def parse_monkey(monkey_text) -> dict:
    lines = monkey_text.splitlines()
    index = int(lines[0].replace(":", "").split()[1])
    items = [int(i) for i in lines[1].split(":")[1].strip().split(", ")]

    return {
        "index": index,
        "items": items,
        "operation": lambda old: old * 19,
        "test": lambda stress: stress % 23 == 0,
        "true_index": 2,
        "false_index": 3,
    }


@pytest.mark.parametrize(
    "text,result",
    [
        (
            dedent(
                """
                Monkey 0:
                  Starting items: 79, 98
                  Operation: new = old * 19
                  Test: divisible by 23
                    If true: throw to monkey 2
                    If false: throw to monkey 3
                """.strip()
            ),
            {
                "index": 0,
                "items": [79, 98],
                "operation": lambda old: old * 19,
                "test": lambda stress: stress % 23 == 0,
                "true_index": 2,
                "false_index": 3,
            },
        ),
        (
            dedent(
                """
                Monkey 1:
                  Starting items: 54, 65, 75, 74
                  Operation: new = old + 6
                  Test: divisible by 19
                    If true: throw to monkey 2
                    If false: throw to monkey 0
                """.strip()
            ),
            {
                "index": 1,
                "items": [54, 65, 75, 74],
                "operation": lambda old: old + 6,
                "test": lambda stress: stress % 23 == 0,
                "true_index": 2,
                "false_index": 0,
            },
        ),
    ],
)
def test_parse_monkey(text: str, result: dict):
    lambda_keys = ("operation", "test")
    parsed_input = {
        k: v(46) if k in lambda_keys else v for k, v in parse_monkey(text).items()
    }
    parsed_result = {k: v(46) if k in lambda_keys else v for k, v in result.items()}
    assert parsed_input == parsed_result


def parse_monkeys(monkeys_text: str):
    return [parse_monkey(monkey_text) for monkey_text in monkeys_text.split("\n\n")]


@pytest.mark.parametrize(
    "text,result",
    [
        (
            dedent(
                """
                Monkey 0:
                  Starting items: 79, 98
                  Operation: new = old * 19
                  Test: divisible by 23
                    If true: throw to monkey 2
                    If false: throw to monkey 3

                Monkey 1:
                  Starting items: 54, 65, 75, 74
                  Operation: new = old + 6
                  Test: divisible by 19
                    If true: throw to monkey 2
                    If false: throw to monkey 0

                Monkey 2:
                  Starting items: 79, 60, 97
                  Operation: new = old * old
                  Test: divisible by 13
                    If true: throw to monkey 1
                    If false: throw to monkey 3

                Monkey 3:
                  Starting items: 74
                  Operation: new = old + 3
                  Test: divisible by 17
                    If true: throw to monkey 0
                    If false: throw to monkey 1
                """.strip()
            ),
            [
                [79, 98],
                [54, 65, 75, 74],
                [79, 60, 97],
                [74],
            ],
        ),
    ],
)
def test_parse_monkey(text: str, result: list[list[int]]):
    assert [monkey["items"] for monkey in parse_monkeys(text)] == result


def process_monkeys(monkeys):
    new_monkeys = monkeys

    pass
