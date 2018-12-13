import copy

def hundreds_digit(num):
    return (num // 100) % 10

def power_level(x, y, sn):
    id = x + 10
    return hundreds_digit(((id * y) + sn) * id) - 5

# returns G, a 300x300 matrix where G[x][y] = power level of cell[x][y]
def grid_power_level(sn):
    grid = [[None for x in range(0, 300)] for y in range(0, 300)]
    for x, row in enumerate(grid):
        for y, val in enumerate(row):
            grid[x][y] = power_level(x, y, sn)
    return grid

# returns S, a 300x300 matrix where S[x][y] = the sum of all G[0..x][0..y]
def summations_grid(grid):
    summations = copy.deepcopy(grid)
    for x in range(0, len(summations)):
        for y in range(0, len(summations[x])):
            if x == 0 and y == 0:
                summations[x][y] = grid[x][y]
            elif x == 0:
                summations[x][y] = grid[x][y] + summations[x][y-1]
            elif y == 0:
                summations[x][y] = grid[x][y] + summations[x-1][y]
            else:
                summations[x][y] = grid[x][y] + summations[x-1][y] + summations[x][y-1] - summations[x-1][y-1]
    return summations

# returns the summation of the power level of a grid of cells starting at G[sx][sy] with a size of sz by sz
def compute_square_sum(grid, summations, sx, sy, sz):
    if sz == 1:
        return grid[sx][sy]
    else:
        tx, ty = sx+sz-1, sy+sz-1
        sum_till_target = summations[tx][ty]
        sum_before_x = 0 if sx == 0 else summations[sx-1][ty]
        sum_before_y = 0 if sy == 0 else summations[tx][sy-1]
        sum_before_xy = 0 if sx == 0 and sy == 0 else summations[sx-1][sy-1]
        return sum_till_target - sum_before_x - sum_before_y + sum_before_xy

# returns the value and starting coordinates of the sub-grid of the given size with the highest value
def compute_best(grid, summations, sz):
    best, bx, by = 0, 0, 0
    for x in range(0, len(grid)-sz):
        for y in range(0, len(grid[x])-sz):
            v = compute_square_sum(grid, summations, x, y, sz)
            if v > best:
                best, bx, by = v, x, y
    return (best, bx, by)

def part1(grid, summations):
    best = compute_best(grid, summations, 3)
    return (best[1], best[2])

def part2(grid, summations):
    best, bx, by, bz = 0, 0, 0, 0

    for sz in range(1, len(grid) + 1):
        (v, vx, vy) = compute_best(grid, summations, sz)
        if v > best:
            best, bx, by, bz = v, vx, vy, sz
    
    return (bx, by, bz)

# ----------------------------------------------------

input = 1788
grid = grid_power_level(input)
summations = summations_grid(grid)

print(part1(grid, summations))
print(part2(grid, summations))