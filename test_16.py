from collections import defaultdict
from textwrap import dedent

import pytest

import util

input_text = util.read_data(16)

short_example = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip()

AA = "AA"
BB = "BB"
CC = "CC"
DD = "DD"
EE = "EE"
FF = "FF"
GG = "GG"
HH = "HH"
II = "II"
JJ = "JJ"


def parse_lines(text: str):
    return {
        line.split()[1]: {
            "tunnels": sorted(
                line.replace("valves", "valve").split("valve")[1].strip().split(", ")
            ),
            "flow_rate": int(line.split("=")[1].split(";")[0]),
        }
        for line in text.splitlines()
    }


@pytest.mark.parametrize(
    "text,result",
    [
        (
            dedent(
                """
                Valve AA has flow rate=0; tunnels lead to valve BB
                Valve BB has flow rate=13; tunnels lead to valves CC, AA
                Valve CC has flow rate=2; tunnels lead to valve BB
                """
            ).strip(),
            {
                "AA": {"flow_rate": 0, "tunnels": ["BB"]},
                "BB": {"flow_rate": 13, "tunnels": ["AA", "CC"]},
                "CC": {"flow_rate": 2, "tunnels": ["BB"]},
            },
        ),
    ],
)
def test_parse_lines(text: str, result):
    assert parse_lines(text) == result


def step(valves, history, states):
    position = 0
    combined_pressure = 1
    open_valves = 2
    pressure_released = 3
    # cf - current flow
    # dp - delta pressure - combined pressure lost
    # o - opened valves
    new_states = defaultdict(list)
    for state in states:
        if (
            state[position] not in state[open_valves]
            and valves[state[position]]["flow_rate"]
        ):
            new_state = (
                state[position],
                state[combined_pressure] + valves[state[position]]["flow_rate"],
                tuple(sorted(state[open_valves] + (state[position],))),
                state[pressure_released] + state[combined_pressure],
            )
            if new_state not in history:
                new_states[new_state[:-1]].append(new_state[-1])

        for new_valve in sorted(valves[state[position]]["tunnels"]):
            new_state = (
                new_valve,
                state[combined_pressure],
                state[open_valves],
                state[pressure_released] + state[combined_pressure],
            )
            if new_state not in history:
                new_states[new_state[:-1]].append(new_state[-1])

    return {k + (max(v),) for k, v in new_states.items()}


@pytest.mark.parametrize(
    "valves,history,states,result",
    [
        (
            {
                "AA": {"flow_rate": 0, "tunnels": ["BB"]},
                "BB": {"flow_rate": 13, "tunnels": ["AA", "CC"]},
                "CC": {"flow_rate": 2, "tunnels": ["BB"]},
            },
            set(),
            {
                ("AA", 0, tuple(), 0),
            },
            {
                # ("AA", 0, 0, ("AA",)),
                ("BB", 0, tuple(), 0),
            },
        ),
        (
            {
                "AA": {"flow_rate": 0, "tunnels": ["BB"]},
                "BB": {"flow_rate": 13, "tunnels": ["AA", "CC"]},
                "CC": {"flow_rate": 2, "tunnels": ["BB"]},
            },
            {
                ("AA", 0, tuple(), 0),
            },
            {
                # ("AA", 0, 0, ("AA",)),
                ("BB", 0, tuple(), 0),
            },
            {
                # ("BB", 0, ("AA",)),
                ("BB", 13, ("BB",), 0),
                ("CC", 0, tuple(), 0),
            },
        ),
        (
            {
                "AA": {"flow_rate": 0, "tunnels": ["BB"]},
                "BB": {"flow_rate": 13, "tunnels": ["AA", "CC"]},
                "CC": {"flow_rate": 2, "tunnels": ["BB"]},
            },
            {
                ("AA", 0, tuple(), 0),
                # ("AA", 0, 0, ("AA",)),
                ("BB", 0, tuple(), 0),
            },
            {
                # ("BB", 0, 0, ("AA",)),
                ("BB", 13, ("BB",), 0),
                ("CC", 0, tuple(), 0),
            },
            {
                # ("BB", 13, 0, ("AA", "BB")),
                # ("CC", 0, 0, ("AA",)),
                ("AA", 13, ("BB",), 13),
                ("CC", 13, ("BB",), 13),
                ("CC", 2, ("CC",), 0),
            },
        ),
    ],
)
def test_step(valves, history, states, result):
    new_states = step(valves, history, states)
    assert new_states == result


def _print_states(states):
    for state in sorted(states):
        print("[" + ", ".join(f"{str(s):>5}" for s in state) + "]")
    print("--")


def walk(valves, start, steps):
    start_state = (start, 0, tuple(), 0)
    states = {start_state}
    history = set()
    for i in range(steps):
        print(i + 1)
        history |= set(states)
        states = step(valves, history, states)
    return states


@pytest.mark.parametrize(
    "valves,steps,result",
    [
        (
            {
                "AA": {"flow_rate": 0, "tunnels": ["BB"]},
                "BB": {"flow_rate": 13, "tunnels": ["AA", "CC"]},
                "CC": {"flow_rate": 2, "tunnels": ["BB"]},
            },
            2,
            {
                # ("BB", 0, 0, ("AA",)),
                ("BB", 13, ("BB",), 0),
                ("CC", 0, tuple(), 0),
            },
        ),
        (
            {
                "AA": {"flow_rate": 0, "tunnels": ["BB"]},
                "BB": {"flow_rate": 13, "tunnels": ["AA", "CC"]},
                "CC": {"flow_rate": 2, "tunnels": ["BB"]},
            },
            3,
            {
                # ("BB", 13, 0, ("AA", "BB")),
                # ("CC", 0, 0, ("AA",)),
                ("AA", 13, ("BB",), 13),
                ("CC", 13, ("BB",), 13),
                ("CC", 2, ("CC",), 0),
            },
        ),
    ],
)
def test_walk(valves, steps, result):
    end_states = walk(valves, "AA", steps)
    assert end_states == result


@pytest.mark.parametrize(
    "text,steps,result",
    [
        (
            dedent(
                """
                Valve AA has flow rate=0; tunnels lead to valves BB
                Valve BB has flow rate=13; tunnels lead to valves CC, AA
                Valve CC has flow rate=2; tunnels lead to valves BB
                """
            ).strip(),
            3,
            {
                # ("BB", 13, 0, ("AA", "BB")),
                # ("CC", 0, 0, ("AA",)),
                ("AA", 13, ("BB",), 13),
                ("CC", 13, ("BB",), 13),
                ("CC", 2, ("CC",), 0),
            },
        ),
        (
            short_example,
            1,
            {
                # (AA, 0, 0, ("AA",)),
                (BB, 0, tuple(), 0),
                (DD, 0, tuple(), 0),
                (II, 0, tuple(), 0),
            },
        ),
        (
            short_example,
            2,
            {
                # (BB, 0, 0, ("AA",)),
                # (DD, 0, 0, ("AA",)),
                # (II, 0, 0, ("AA",)),
                (CC, 0, tuple(), 0),
                (CC, 0, tuple(), 0),
                (EE, 0, tuple(), 0),
                (JJ, 0, tuple(), 0),
                (BB, 13, ("BB",), 0),
                (DD, 20, ("DD",), 0),
            },
        ),
        (
            short_example,
            3,
            {
                (CC, 20, ("DD",), 20),
            },
        ),
        (
            short_example,
            5,
            {
                (BB, 33, ("BB", "DD"), 60),
            },
        ),
        (
            short_example,
            20,
            {
                (EE, 76, ("BB", "DD", "HH", "JJ"), 624 + 76 * 3),
            },
        ),
        (
            short_example,
            23,
            {
                (CC, 79, (BB, DD, EE, HH, JJ), 624 + 76 * 4 + 79 * 2),
            },
        ),
    ],
)
def test_walk_text(text, steps, result):
    valves = parse_lines(text)
    end_states = walk(valves, "AA", steps)
    for state in result:
        assert state in end_states


@pytest.mark.parametrize(
    "text,steps,result",
    [
        (
            short_example,
            20,
            624 + 76 * 3,
        ),
        (
            short_example,
            23,
            624 + 76 * 4 + 79 * 2,
        ),
        (
            short_example,
            30,
            1651,
        ),
        (
            input_text,
            30,
            1789,
        ),
    ],
)
def test_part1(text, steps, result):
    valves = parse_lines(text)
    end_states = walk(valves, "AA", steps)
    max_pressure = max(s[-1] for s in end_states)
    assert max_pressure == result
