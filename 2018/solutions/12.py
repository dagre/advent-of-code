import copy
import re

def parse(str):
    return [False if s == '.' else True for s in str if s in ['.', '#']]

def load_file(path):
    initial_state = None
    configurations = {}
    with open(path) as fp:
        # initial line
        line = fp.readline()

        start_index = min([line.find('.'), line.find('#')])
        initial_state = parse(line[start_index:len(line)])

        # separator
        line = fp.readline()

        # configurations
        line = fp.readline()
        while line:
            arrow_index = line.find(' => ')
            configuration = line[0:arrow_index]
            next_gen_value = parse(line[arrow_index+4:len(line)])[0]
            if next_gen_value:
                configurations[tuple(parse(configuration))] = True
            
            line = fp.readline()
    return initial_state, configurations

def tupleize(state, index, offset):
    values = []
    for i in range(index-offset, index+offset+1):
        values.append(state[i])
    return tuple(values)

def add_falses(arr, how_many, start):
    for i in range(0, how_many):
        if start:
            arr.insert(0, False)
        else:
            arr.append(False)
    return arr

def wrap_state_with_falses(state):
    offset_moved = 0
    if state[0]:
        state = add_falses(state, 3, True)
        offset_moved = 3
    elif state[1]:
        state = add_falses(state, 2, True)
        offset_moved = 2
    elif state[2]:
        state = add_falses(state, 1, True)
        offset_moved = 1
    
    if state[len(state)-1]:
        state = add_falses(state, 3, False)
    elif state[len(state)-2]:
        state = add_falses(state, 2, False)
    elif state[len(state)-3]:
        state = add_falses(state, 1, False)
    
    return state, offset_moved

def trim_state(state, zero_index):
    trim_beginning = 0
    trim_end = 0

    for s in state:
        if not s:
            trim_beginning += 1
        else:
            break
    
    for s in range(len(state)-1, 0, -1):
        if not state[s]:
            trim_end += 1
        else:
            break
    
    return state[trim_beginning:(len(state) - trim_end)], zero_index - trim_beginning

def iteration(zero_index, state, configurations):
    offset=2
    state, offset_moved = wrap_state_with_falses(state)
    new_zero_index = zero_index + offset_moved
    state_after = copy.copy(state)
    for i in range(offset, len(state)-offset):
        configuration = tupleize(state, i, offset)
        state_after[i] = configurations.get(configuration, False)
    
    ta, tb = trim_state(state_after, new_zero_index)
    print_iteration(ta, tb)
    return ta, tb

def print_iteration(state, zero_index):
    s = ''
    if zero_index < 0:
        s += '<<' + str(zero_index) + "|"
    for i, p in enumerate(state):
        s += '[' if i==zero_index else ''
        s += '#' if p else '.'
        s += ']' if i==zero_index else ''
    print(s)

def iterate_n(zero_index, state, configurations, num_iterations):
    history = []
    s, z = state, zero_index
    for i in range(0, num_iterations):
        s, z = iteration(z, s, configurations)
        history.append((copy.copy(s), z))

        pattern = identify_pattern(history, i, num_iterations)
        if pattern:
            return pattern

    return s, z

def identify_pattern(history, current_i, target_i):
    lb = 50
    start_index = len(history)-lb

    if start_index > 1:
        target = history[start_index][0]
        delta = history[start_index][1] - history[start_index-1][1]
        for i in range(start_index+1, len(history)):
            if history[i][0] != target or history[i][1] - history[i-1][1] != delta:
                return None
        
        # at current_i, value is history[len(history)-1]
        # each step, the value is moving by delta
        # we want the value at target_i - 1
        
        steps_until_done = (target_i - 1) - current_i
        delta_applied_until_done = steps_until_done * delta
        value_when_done = history[len(history)-1][1] + delta_applied_until_done

        print('pattern identified!')
        print_iteration(history[len(history)-1][0], value_when_done)
        return (history[len(history)-1][0], value_when_done)

def filled_pot_sum(state, zero_index):
    sum = 0
    for i, p in enumerate(state):
        pot_index = i - zero_index
        if p:
            sum += pot_index
    return sum

def part1(initial_state, configurations):
    s,z = iterate_n(0, initial_state, configurations, 20)
    return filled_pot_sum(s, z)

def part2(initial_state, configurations):
    s,z = iterate_n(0, initial_state, configurations, 50000000000)
    return filled_pot_sum(s, z)

# test data
test_initial_state = parse('#..#.#..##......###...###')
test_configuration_keys = [tuple(parse(s)) for s in ['...##', '..#..', '.#...', '.#.#.', '.#.##', '.##..', '.####', '#.#.#', '#.###', '##.#.', '##.##', '###..', '###.#', '####.']]
test_configurations = {}
for k in test_configuration_keys:
    test_configurations[k] = True

initial_state, configurations = load_file('2018/input/input-12a.txt')

print('test:', part1(test_initial_state, test_configurations))

print(part1(initial_state, configurations))
print(part2(initial_state, configurations))
