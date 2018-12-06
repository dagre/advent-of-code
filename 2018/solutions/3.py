import cairo
import re

claim_pattern = re.compile(r'#([0-9]*) @ ([0-9]*),([0-9]*): ([0-9]*)x([0-9]*)')

class Claim:
    def __init__(self, id, dl, dt, w, h):
        self.id = int(id)
        self.dl = int(dl)
        self.dt = int(dt)
        self.w = int(w)
        self.h = int(h)

def parse(claim):
    groups = claim_pattern.findall(claim)
    (id, dl, dt, w, h) = groups[0]
    return Claim(id, dl, dt, w, h)

def load_file(path):
    lines = []
    with open(path) as fp:
        line = fp.readline()
        while line:
            lines.append(parse(line))
            line = fp.readline()
    return lines

lines = load_file('input-3a.txt')

def count(grid):
    matches = 0
    for i in grid:
        for j in i:
            if j >= 2:
                matches += 1
    return matches

def part1():
    grid = [[0 for i in range(0,1000)] for j in range(0,1000)]
    for claim in lines:
        for h in range(claim.dl, claim.dl+claim.w):
            for v in range(claim.dt, claim.dt+claim.h):
                grid[h][v] += 1
    
    return count(grid)

def part2():
    grid = [[[] for i in range(0,1000)] for j in range(0,1000)]
    non_overlapping = set()
    for claim in lines:
        non_overlapping.add(claim.id)
        for h in range(claim.dl, claim.dl+claim.w):
            for v in range(claim.dt, claim.dt+claim.h):
                grid[h][v].append(claim.id)
                if (len(grid[h][v]) != 1):
                    for elem in grid[h][v]:
                        if elem in non_overlapping:
                            non_overlapping.remove(elem)
    return non_overlapping

print(part1())
print(part2())

def show(areas):
    with cairo.SVGSurface('3.svg', 1000, 1000) as surface:
        context = cairo.Context(surface)
        context.scale(1,1) # 1 unit = 1 unit
        context.set_line_width(1)
        for claim in areas:
            # highlight the solution for part 2
            if claim.id == 775:
                r = 1
            else:
                r = 0
            
            context.set_source_rgba(r,0,0,1)
            context.rectangle(claim.dl, claim.dt, claim.w, claim.h)
            context.stroke_preserve()
            context.set_source_rgba(r,0,0,0.4)
            context.fill()

show(lines)