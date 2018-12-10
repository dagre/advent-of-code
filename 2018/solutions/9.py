import re

pattern = re.compile(r'([0-9]*) players; last marble is worth ([0-9]*) points')

def parse(str):
    groups = pattern.findall(str)
    (np, lm) = groups[0]
    return (int(np), int(lm))

def load_file(path):
    lines = []
    with open(path) as fp:
        line = fp.readline()
        return parse(line)

(num_players, num_marbles) = load_file('input/input-9a.txt')

def index(i, list):
    while i < 0:
        i += 100*len(list)
        # make sure it is in range
    return i % len(list)

def play(num_players, num_marbles):
    scores = [0 for i in range(0, num_players)]
    curr_player_index = 0
    marbles = [0]
    curr_marble_index = 0

    for next_marble_num in range(1, num_marbles+1):
        new_current_marble_index = None
        if next_marble_num % 23 != 0:
            new_current_marble_index = index(curr_marble_index + 2, marbles)
            marbles.insert(new_current_marble_index, next_marble_num)
        else:
            scores[curr_player_index] += next_marble_num
            popped_marble_index = index(curr_marble_index - 7, marbles)
            scores[curr_player_index] += marbles.pop(popped_marble_index)
            new_current_marble_index = popped_marble_index
        
        curr_player_index = index(curr_player_index+1, scores)
        curr_marble_index = new_current_marble_index

    return scores

def part1(np, nm):
    return max(play(np, nm))

def part2(np, nm):
    return max(play(np, nm*100))

print(part1(num_players, num_marbles))
print(part2(num_players, num_marbles)) # very, very, very slow