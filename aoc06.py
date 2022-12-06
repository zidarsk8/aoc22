import util

text = util.read_data(6)
print(text)


# bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
# nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
# nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
# zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11

# text = "bvwbjplbgvbhsrlpgdmjqwftvncz"
# text = "nppdvjthqldpwncqszvftbrmjlhg"
# text = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
# text = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"


n = 14
fours = list(zip(text[:-3], text[1:-2], text[2:-1], text[3:]))
fours = list(zip(*[text[i : len(text) - n + i] for i in range(n)]))
print(fours)

for i, f in enumerate(fours):
    if len(set(f)) == n:
        print(i + n, f)
        break
