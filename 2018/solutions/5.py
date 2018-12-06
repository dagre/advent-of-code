def load_file(path):
    with open(path) as fp:
        return fp.readline()

polymer = load_file('input/input-5a.txt').strip()

def same_unit(a,b):
    different_polarity = (a.isupper() and b.islower()) or (a.islower() and b.isupper())
    same_type = (a.lower() == b.lower())
    return same_type and different_polarity

def extract_lower_units(polymer):
    units = set()
    for c in polymer:
        units.add(c.lower())
    return units

def react(polymer):
    units = extract_lower_units(polymer)
    changed = True
    while changed:
        before = len(polymer)
        for c in units:
            repstr = c + c.upper()
            repstr2 = c.upper() + c
            polymer = polymer.replace(repstr, '').replace(repstr2, '')
        after = len(polymer)
        changed = (before != after)
    
    return polymer
            
def part1(polymer):
    return len(react(polymer))

def part2(polymer):
    units = extract_lower_units(polymer)
    scores = {}
    for c in units:
        candidate = polymer.replace(c, '').replace(c.upper(), '')
        scores[c] = len(react(candidate))
    return min(scores.values())

print(part1(polymer))
print(part2(polymer))
