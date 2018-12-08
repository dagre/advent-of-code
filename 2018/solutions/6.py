import re

coord_pattern = re.compile(r'([0-9]*), ([0-9]*)')

def parse(str):
    groups = coord_pattern.findall(str)
    (x,y) = groups[0]
    return (int(x), int(y))

def load_file(path):
    lines = []
    with open(path) as fp:
        line = fp.readline()
        while line:
            lines.append(parse(line))
            line = fp.readline()
    return lines

def manhattan(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def closest(x, y, points):
    mind = 999
    mins = []
    for px, py in points:
        d = manhattan(x,y,px,py)
        if d < mind:
            mind = d
            mins = [(px, py)]
        elif d == mind:
            mins.append((px, py))
    return mins

def part1():
    lines = load_file('input/input-6a.txt')
    sz = 400
    grid = [[None for x in range(0,sz)] for y in range(0,sz)]
    areas = {}
    for x in range(0, sz):
        for y in range(0, sz):
            pc = closest(x,y, lines)
            if len(pc) == 1:
                (cx, cy) = pc[0]
                grid[x][y] = (cx, cy)
                if (cx, cy) not in areas:
                    areas[(cx, cy)] = {
                        'sum_p': 0,
                        'infinite': False
                    }
                areas[(cx, cy)]['sum_p'] += 1
                if x == 0 or y == 0 or x == sz-1 or y == sz-1:
                    areas[(cx, cy)]['infinite'] = True

    return max(filter(lambda t: not t[1]['infinite'], areas.items()), key = lambda t2: t2[1]['sum_p'])[1]['sum_p']

def part2():
    points = load_file('input/input-6a.txt')
    sz = 400
    target = 10000
    valid_points = []
    for x in range(0,sz):
        for y in range(0,sz):
            sumd = 0
            for px, py in points:
                sumd += manhattan(x,y,px,py)
            if sumd < target:
                valid_points.append((x,y))
    return len(valid_points)

print(part1())
print(part2())