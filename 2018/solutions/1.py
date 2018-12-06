def load_file(path):
    lines = []
    with open(path) as fp:
        line = fp.readline()
        while line:
            lines.append(int(line))
            line = fp.readline()
    return lines

def do_iter(start, values):
    for v in values:
        start += v
    return start

def part1():
    lines = load_file('input-1a.txt')
    return do_iter(0, lines)

def part2():
    lines = load_file('input-1a.txt')
    occurrences = {}
    value = 0
    index = 0
    while True:
        value = value + lines[index%len(lines)]
        index += 1
        if not value in occurrences:
            occurrences[value] = 1
        else:
            occurrences[value]+=1
        if occurrences[value] == 2:
            return value

print(part1())
print(part2())