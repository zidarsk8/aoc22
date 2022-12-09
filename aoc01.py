import util

cals = util.read_data(1)


single_line = " ".join(cals.splitlines())

print(single_line)

elves = single_line.split("  ")

elves_cals = [list(map(int, elve.split())) for elve in elves]
print(elves_cals)

sums = sorted([sum(elve) for elve in elves_cals])

print(sums[-5:])
print(max(sums))
print(sum(sums[-3:]))
