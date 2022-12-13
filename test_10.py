import pytest

import util

FULL_TEXT = util.read_data(10)


short_example = """noop
addx 3
addx -5"""

long_example = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

from icecream import ic


def part1(lines):
    x = 1
    cycle = 0
    signal = 0
    ic(lines)

    for line in lines:
        ic("-------------")
        ic(line)
        ic(cycle)
        ic(signal)
        if line == "noop":
            cycle += 1
            if cycle % 20 == 0:
                yield x * cycle
        if line.startswith("addx"):
            cycle += 1
            if cycle % 20 == 0:
                yield x * cycle
            cycle += 1
            if cycle % 20 == 0:
                yield x * cycle
            x += int(line.split()[1])

        ic(line)
        ic(cycle)
        ic(signal)

    return signal


@pytest.mark.parametrize(
    "text,result",
    [
        (short_example.splitlines(), []),
        (long_example.splitlines()[:20], [420]),
        (long_example.splitlines()[:50], [420, 40, 1140, 2960]),
    ],
)
def test_draw_grid(text, result):
    assert list(part1(text)) == result


def sum_signals(signals, positions):
    return sum(signals[p // 20 - 1] for p in positions if p // 20 - 1 < len(signals))


@pytest.mark.parametrize(
    "text,result",
    [
        (long_example.splitlines()[:20], 420),
        (long_example.splitlines(), 13140),
        (FULL_TEXT.splitlines(), 13760),
    ],
)
def test_part_sum(text, result):
    assert sum_signals(list(part1(text)), [20, 60, 100, 140, 180, 220]) == result


def register_values(lines):
    x = 1
    cycle = 0
    signal = 0

    for line in lines:
        if line == "noop":
            yield x
        if line.startswith("addx"):
            yield x
            yield x
            x += int(line.split()[1])

    return x


# long_example = """addx 15
# addx -11
# addx 6
# addx -3
# addx 5
# """
@pytest.mark.parametrize(
    "text,result",
    [
        (short_example.splitlines(), [1, 1, 1, 4, 4]),
        (long_example.splitlines()[:6], [1, 1, 16, 16, 5, 5, 11, 11, 8, 8, 13, 13]),
    ],
)
def test_part2_register_values(text, result):
    assert list(register_values(text)) == result


def draw(lines, cycles: int):
    line_length = 40
    x = list(register_values(lines))

    draw_data = zip(x[:cycles], [x % line_length for x in range(cycles)])

    pixels = ["#" if abs(a - b) < 2 else "." for a, b in draw_data]
    line = "".join(pixels)
    return "\n".join(
        line[i : i + line_length] for i in range(0, len(line), line_length)
    )


@pytest.mark.parametrize(
    "text,cycles,result",
    [
        (long_example.splitlines(), 20, "##..##..##..##..##.."),
        (long_example.splitlines(), 40, "##..##..##..##..##..##..##..##..##..##.."),
        (
            long_example.splitlines(),
            80,
            "##..##..##..##..##..##..##..##..##..##..\n"
            "###...###...###...###...###...###...###.",
        ),
        (
            long_example.splitlines(),
            240,
            """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....""",
        ),
        (
            FULL_TEXT.splitlines(),
            240,
            """
###..####.#..#.####..##..###..####.####.
#..#.#....#.#.....#.#..#.#..#.#....#....
#..#.###..##.....#..#....#..#.###..###..
###..#....#.#...#...#....###..#....#....
#.#..#....#.#..#....#..#.#....#....#....
#..#.#....#..#.####..##..#....####.#....
""".strip(),
        ),
    ],
)
def test_draw(text, cycles, result):
    assert draw(text, cycles) == result
