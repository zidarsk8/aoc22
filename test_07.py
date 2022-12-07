import util


def get_code(text):
    return 0


def get_structure(lines):
    struc = {}
    if not lines:
        return struc
    line = lines.pop(0)
    if line.startswith("$ cd"):
        return {line.split()[2]: get_structure(lines)}
    elif line.startswith("$ ls"):
        while lines and not lines[0].startswith("$ "):
            line = lines.pop(0)
            if line.startswith("dir "):
                struc[line.split()[1]] = {}
            else:
                struc[line.split()[1]] = int(line.split()[0])

    return struc

def test_structure_basic():
    assert get_structure([""]) == {}
    assert get_structure([]) == {}


def test_structure_root():
    assert get_structure("$ cd /".splitlines()) == {"/": {}}


def test_structure_ls_empty():
    lines = ["$ cd /",
             "$ ls"]
    assert get_structure(lines) == {"/": {}}

def test_structure_ls_file():
    lines = [
        "$ cd /",
         "$ ls",
         "3 file1.txt"
    ]
    assert get_structure(lines) == {"/": {"file1.txt":3}}

def test_structure_ls_dir():
    lines = [
        "$ cd /",
         "$ ls",
         "dir b"
    ]
    assert get_structure(lines) == {"/": {"b":{}}}

def test_structure_ls_dir_file():
    lines = [
        "$ cd /",
         "$ ls",
         "dir b",
         "5 a.txt",
         "dir c",
    ]
    assert get_structure(lines) == {"/": {"a.txt": 5, "c":{},"b":{}}}

