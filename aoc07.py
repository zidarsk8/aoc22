from icecream import ic

import util

text = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


text = util.read_data(7)

lines = text.splitlines()
lines.pop(0)

current_loc = ("/",)
structure = {current_loc: {}}

while lines:
    line = lines.pop(0)
    ic(line)
    if line == "$ ls":
        pass
    elif line.startswith("dir"):
        structure[current_loc + (line.split()[1],)] = {}
    elif line == "$ cd ..":
        current_loc = current_loc[:-1]
    elif line.startswith("$ cd "):
        current_loc = current_loc + (line.split()[2],)
    else:
        structure[current_loc][line.split()[1]] = line.split()[0]


sizes = [ic(sum(map(int, files.values()))) for d, files in structure.items()]
ic(structure)
print(sum(size for size in sizes if size < 100000))

# sizes
for k in sorted(structure.keys(), reverse=True):
    files = [v for k, v in structure[k].items() if k != "_"]
    file_sizes = sum(map(int, structure[k].values()))
    structure[k]["_"] = file_sizes
    if k[:-1]:
        structure[k[:-1]]["_"] = structure[k[:-1]].get("_", 0) + file_sizes

small_dirs = sum(v["_"] for v in structure.values() if v["_"] < 100000)

ic(small_dirs)

ic(structure[("/",)]["_"])

free_space = 70000000 - structure[("/",)]["_"]
ic(free_space)
missing_space = 30000000 - free_space
ic(missing_space)

all_dir_sizes = sorted([v["_"] for v in structure.values() if v["_"] > missing_space])
ic(all_dir_sizes)
