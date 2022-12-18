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

v_map = {
    8: 60,
    10: 80,
    # 13: 90,
}


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


non_zero_valves = {
    10: 6,
    59: 15,
}


def filter_states(states):

    seen = defaultdict(dict)
    for pos, rate, opened, flow in states:
        seen[pos][opened] = (rate, flow)

    result = set()
    for pos, group in seen.items():
        group_sets = [set(k) for k in group]
        for k, item in group.items():
            if any(set(k) < s for s in group_sets):
                continue
            result.add((pos, item[0], k, item[1]))

    return result


@pytest.mark.parametrize(
    "states,result",
    [
        (
            {
                (("ZD", "ZR"), 4, ("OF",), 16),
                (("ZD", "ZR"), 7, ("LG", "OF"), 19),
                (("ZD", "ZR"), 8, ("DC",), 8),
                (("ZD", "ZR"), 9, ("UE",), 27),
                (("ZD", "ZR"), 11, ("DC", "LG"), 11),
                (("ZD", "ZR"), 12, ("LG", "UE"), 30),
                (("ZD", "ZR"), 14, ("LG", "OF", "ZE"), 47),
                (("ZZ", "ZZ"), 17, ("MB",), 68),
                (("ZZ", "ZZ"), 19, ("LG", "TL"), 28),
                (("ZZ", "ZZ"), 20, ("LG", "MB"), 80),
                (("ZZ", "ZZ"), 23, ("TL", "ZE"), 44),
                (("ZZ", "ZZ"), 24, ("MB", "ZE"), 96),
                (("ZZ", "ZZ"), 26, ("LG", "TL", "ZE"), 56),
                (("ZZ", "ZZ"), 33, ("MB", "TL"), 84),
                (("ZZ", "ZZ"), 36, ("LG", "MB", "TL"), 96),
            },
            {
                (("ZD", "ZR"), 11, ("DC", "LG"), 11),
                (("ZD", "ZR"), 12, ("LG", "UE"), 30),
                (("ZD", "ZR"), 14, ("LG", "OF", "ZE"), 47),
                (("ZZ", "ZZ"), 24, ("MB", "ZE"), 96),
                (("ZZ", "ZZ"), 26, ("LG", "TL", "ZE"), 56),
                (("ZZ", "ZZ"), 36, ("LG", "MB", "TL"), 96),
            },
        ),
    ],
)
def test_filter_states(states, result):
    filtered = filter_states(states)
    _print_states(filtered)
    _print_states(result)
    assert filtered == result


def step(valves, history, states, i=None):
    position = 0
    combined_pressure = 1
    open_valves = 2
    pressure_released = 3
    # cf - current flow
    # dp - delta pressure - combined pressure lost
    # o - opened valves
    new_states = defaultdict(list)
    for state in states:
        if len(state[open_valves]) == non_zero_valves.get(len(valves), len(valves)):
            new_state = (
                state[position],
                state[combined_pressure],
                state[open_valves],
                state[pressure_released] + state[combined_pressure],
            )
            new_states[new_state[:-1]].append(new_state[-1])
            continue
        if (
            state[position][0] not in state[open_valves]
            and valves[state[position][0]]["flow_rate"]
        ):

            if (
                state[position][1] not in state[open_valves]
                and valves[state[position][1]]["flow_rate"]
                and state[position][0] != state[position][1]
            ):

                new_state = (
                    state[position],
                    state[combined_pressure]
                    + valves[state[position][0]]["flow_rate"]
                    + valves[state[position][1]]["flow_rate"],
                    tuple(sorted(set(state[open_valves] + state[position]))),
                    state[pressure_released] + state[combined_pressure],
                )
                if new_state not in history:
                    new_states[new_state[:-1]].append(new_state[-1])

            for new_valve_1 in sorted(valves[state[position][1]]["tunnels"]):
                new_state = (
                    tuple(sorted((state[position][0], new_valve_1))),
                    state[combined_pressure] + valves[state[position][0]]["flow_rate"],
                    tuple(sorted(set(state[open_valves] + (state[position][0],)))),
                    state[pressure_released] + state[combined_pressure],
                )
                if new_state not in history:
                    new_states[new_state[:-1]].append(new_state[-1])

        for new_valve_0 in sorted(valves[state[position][0]]["tunnels"]):

            if (
                state[position][1] not in state[open_valves]
                and valves[state[position][1]]["flow_rate"]
            ):

                new_state = (
                    tuple(sorted((new_valve_0, state[position][1]))),
                    state[combined_pressure] + valves[state[position][1]]["flow_rate"],
                    tuple(sorted(set(state[open_valves] + (state[position][1],)))),
                    state[pressure_released] + state[combined_pressure],
                )
                if new_state not in history:
                    new_states[new_state[:-1]].append(new_state[-1])

            for new_valve_1 in sorted(valves[state[position][1]]["tunnels"]):
                new_state = (
                    tuple(sorted((new_valve_0, new_valve_1))),
                    state[combined_pressure],
                    state[open_valves],
                    state[pressure_released] + state[combined_pressure],
                )
                if new_state not in history:
                    new_states[new_state[:-1]].append(new_state[-1])

    max_states = {
        k + (max(v),) for k, v in new_states.items() if k[1] > v_map.get(i, -1)
    }

    return filter_states(max_states)


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
                (("AA", "AA"), 0, tuple(), 0),
            },
            {
                (("BB", "BB"), 0, tuple(), 0),
            },
        ),
        (
            {
                "AA": {"flow_rate": 0, "tunnels": ["BB"]},
                "BB": {"flow_rate": 13, "tunnels": ["AA", "CC"]},
                "CC": {"flow_rate": 2, "tunnels": ["BB"]},
            },
            {
                (("AA", "AA"), 0, tuple(), 0),
            },
            {
                (("BB", "BB"), 0, tuple(), 0),
            },
            {
                ((AA, BB), 13, (BB,), 0),
                ((BB, CC), 13, (BB,), 0),
                ((AA, CC), 0, tuple(), 0),
                ((CC, CC), 0, tuple(), 0),
            },
        ),
    ],
)
def test_step(valves, history, states, result):
    new_states = step(valves, history, states)
    assert new_states == result


def _print_states(states):
    for state in sorted(states):
        print("(" + ", ".join(f"{str(s):>5}" for s in state) + "),")
    print("--")


def walk(valves, start, steps):
    start_state = ((start, start), 0, tuple(), 0)
    states = {start_state}
    history = set()
    for i in range(steps):
        print(i + 1)
        history |= set(states)
        states = step(valves, history, states, i)
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
                ((AA, BB), 13, (BB,), 0),
                ((BB, CC), 13, (BB,), 0),
                ((AA, CC), 0, tuple(), 0),
                ((CC, CC), 0, tuple(), 0),
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
                (("AA", "BB"), 13, ("BB",), 13),
                (("AA", "CC"), 15, ("BB", "CC"), 13),
                (("BB", "CC"), 2, ("CC",), 0),
                (("BB", "CC"), 13, ("BB",), 13),
                (("CC", "CC"), 15, ("BB", "CC"), 13),
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
                (("AA", "BB"), 13, ("BB",), 13),
                (("AA", "CC"), 15, ("BB", "CC"), 13),
                (("BB", "CC"), 2, ("CC",), 0),
                (("BB", "CC"), 13, ("BB",), 13),
                (("CC", "CC"), 15, ("BB", "CC"), 13),
            },
        ),
        (
            short_example,
            1,
            {
                (("DD", "II"), 0, (), 0),
            },
        ),
        (
            short_example,
            2,
            {
                (("DD", "JJ"), 20, (DD,), 0),
            },
        ),
        (
            short_example,
            3,
            {
                (("EE", "JJ"), 41, (DD, JJ), 20),
            },
        ),
        (
            short_example,
            4,
            {
                (("FF", "II"), 41, (DD, JJ), 61),
            },
        ),
        (
            short_example,
            5,
            {
                (("AA", "GG"), 41, (DD, JJ), 102),
            },
        ),
        (
            short_example,
            9,
            {
                (("CC", "FF"), 78, ("BB", "CC", "DD", "HH", "JJ"), 336),
            },
        ),
        (
            short_example,
            10,
            {
                (("BB", "EE"), 78, ("BB", "CC", "DD", "HH", "JJ"), 336 + 78),
            },
        ),
        (
            short_example,
            11,
            {
                (("CC", "EE"), 81, ("BB", "CC", "DD", "EE", "HH", "JJ"), 336 + 78 * 2),
            },
        ),
        (
            short_example,
            12,
            {
                (
                    ("CC", "EE"),
                    81,
                    ("BB", "CC", "DD", "EE", "HH", "JJ"),
                    492 + 81,
                ),
            },
        ),
        (
            short_example,
            13,
            {
                (
                    ("CC", "EE"),
                    81,
                    ("BB", "CC", "DD", "EE", "HH", "JJ"),
                    492 + 81 * 2,
                ),
            },
        ),
        (
            short_example,
            26,
            {
                (
                    ("CC", "EE"),
                    81,
                    ("BB", "CC", "DD", "EE", "HH", "JJ"),
                    492 + 81 * 15,
                ),
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
            26,
            1707,
        ),
        (
            input_text,
            15,
            1789,
        ),
    ],
)
def test_part1(text, steps, result):
    valves = parse_lines(text)
    end_states = walk(valves, "AA", steps)
    s = sorted(
        [(rate, pressure, opened, pos) for pos, rate, opened, pressure in end_states]
    )
    _print_states(s)
    print(len(valves))
    print(len([v for v in valves.values() if v["flow_rate"]]))
    print([v["flow_rate"] for v in valves.values() if v["flow_rate"]])
    print(sum([v["flow_rate"] for v in valves.values() if v["flow_rate"]]))
    print(len(s))
    max_pressure = max(s[-1] for s in end_states)
    assert max_pressure == result
