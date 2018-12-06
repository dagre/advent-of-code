def load_file(path):
    lines = []
    with open(path) as fp:
        line = fp.readline()
        while line:
            lines.append(line)
            line = fp.readline()
    return lines

def checksum(lines):
    two = 0
    three = 0
    for line in lines:
        occurrences = {}
        for char in line:
            if not char in occurrences:
                occurrences[char] = 1
            else:
                occurrences[char] += 1
        is_two = False
        is_three = False                
        for _,v in occurrences.items():
            if v == 2:
                is_two = True
            if v == 3:
                is_three = True
        if is_two:
            two += 1
        if is_three:
            three += 1
    return two*three

def distance(s1, s2):
    iterlen = min(len(s1), len(s2))
    distance = abs(len(s1) - len(s2))
    for i in range(0, iterlen):
        if s1[i] != s2[i]:
            distance +=1
    return distance

def keep_same(s1, s2):
    common = ''
    for i in range(0, min(len(s1), len(s2))):
        if s1[i] == s2[i]:
            common += s1[i]
    return common

def part1():
    lines = load_file('input/input-2a.txt')
    return checksum(lines)

def part2():
    lines = load_file('input/input-2a.txt')
    min_delta = 100
    min_delta_from = ''
    min_delta_to = ''
    for frm in lines:
        for to in lines:
            if frm != to:
                d = distance(frm, to)
                if d < min_delta:
                    min_delta = d
                    min_delta_from = frm
                    min_delta_to = to
    return keep_same(min_delta_from, min_delta_to)

print(part1())
print(part2())