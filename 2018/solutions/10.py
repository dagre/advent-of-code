import re
import math
import copy

pattern = re.compile(r'position=<\s*(\-?[0-9]*),\s*(\-?[0-9]*)> velocity=<\s*(\-?[0-9]*),\s*(\-?[0-9]*)>')

def parse(str):
    groups = pattern.findall(str)
    (posx, posy, velx, vely) = groups[0]
    return (int(posx), int(posy), int(velx), int(vely))

def load_file(path):
    lines = []
    with open(path) as fp:
        line = fp.readline()
        while line:
            lines.append(parse(line))
            line = fp.readline()
    return lines

points = load_file('input/input-10a.txt')

def endpoints(points):
    minx, miny = points[0][0], points[0][1]
    maxx, maxy = points[0][0], points[0][1]
    for px, py, vx, vy in points:
        if px < minx:
            minx = px
        if px > maxx:
            maxx = px
        if py < miny:
            miny = py
        if py > maxy:
            maxy = py
    return (minx, miny, maxx, maxy)

def maxd(points):
    (minx, miny, maxx, maxy) = endpoints(points)
    return math.sqrt(math.pow(maxx-minx, 2)+math.pow(maxy-miny, 2))

def move(points):
    for pi, p in enumerate(points):
        (px, py, vx, vy) = p
        points[pi] = (px+vx, py+vy, vx, vy)

def print_sample(sample, t):
    (minx, miny, maxx, maxy) = endpoints(sample)
    print('============================================================================================================')
    print('At t=',t)
    print('============================================================================================================')
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            found = False
            for px, py, vx, vy in sample:
                if px == x and py == y:
                    found = True
                    break
            if found:
                print('#', end='')
            else:
                print('.', end='')
        print('')
    print('')

def get_closest_configuration(points):
    num_samples = 0
    samples = []
    t = 1
    while num_samples == 0 or maxd(points) < 500:
        # keep iterating until we have a sample and the maximum distance between the points exceeds what is reasonable for a message to appear
        move(points)
        if maxd(points) < 100:
            num_samples += 1
            samples.append((copy.copy(points), t))
        t += 1
        
    (min_sample, min_sample_time) = min(samples, key=lambda p: maxd(p[0]))
    return (min_sample, min_sample_time)


(c, ct) = get_closest_configuration(points)
print_sample(c, ct)