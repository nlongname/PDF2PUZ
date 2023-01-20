# Testing whether a generated grid meets general integrity standards
# probably including desired size

# Tests, from easy to hard:
# no outer edges should be all black (all '.')
# outer edges shouldn't be all blank (all 'X') unless the shape dictates it
# symmetry (usually rotational, but sometimes diagonal or vertical or horizontal)
# if it's a little off, what do you do? (multiple clue lists? ask user?)

import numpy as np


def clean_edges(input_grid, target_size=(15, 15)):
    grid = np.array([[char for char in line] for line in input_grid])
    if grid.shape == target_size:
        grid = [''.join(line) for line in grid]  # just in case it's in the pre-split format, still works if it's not
        return grid, None
    not_done = True
    while not_done:  # clear all-black lines first
        not_done = False
        if np.all(grid[:, 0] == '.'):
            grid = grid[:, 1:]
            not_done = True
        if np.all(grid[:, -1] == '.'):
            grid = grid[:, :-1]
            not_done = True
        if np.all(grid[0, :] == '.'):
            grid = grid[1:, :]
            not_done = True
        if np.all(grid[-1, :] == '.'):
            grid = grid[:-1, :]
            not_done = True
    blanks_removed = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # for debugging now, but might use it later
    not_done = True
    while not_done:  # then all-white lines
        # doing all-white separately and after all-black works better for small, sparse puzzles like NYT Minis
        not_done = False
        if not np.any(grid[:, 0] == '.'):
            blanks_removed['left'] += 1
            grid = grid[:, 1:]
            not_done = True
        if not np.any(grid[:, -1] == '.'):
            blanks_removed['right'] += 1
            grid = grid[:, :-1]
            not_done = True
        if not np.any(grid[0, :] == '.'):
            blanks_removed['top'] += 1
            grid = grid[1:, :]
            not_done = True
        if not np.any(grid[-1, :] == '.'):
            blanks_removed['bottom'] += 1
            grid = grid[:-1, :]
            not_done = True
    if grid.shape == target_size:
        blanks_removed = None
    grid = [''.join(line) for line in grid]
    return grid, blanks_removed


def check_rotational(input_grid):
    grid = np.array([[char for char in line] for line in input_grid])
    rotated_grid = np.rot90(grid, 2)
    if rotated_grid == grid:
        return input_grid
    return find_offset(grid, rotated_grid)  # fixed grid or none


def check_diagonal(input_grid):
    grid = np.array([[char for char in line] for line in input_grid])
    flipped_grid = np.transpose(grid)
    temp = find_offset(grid, flipped_grid)
    return temp if temp else np.flip(find_offset(np.flip(grid, 0), np.flip(flipped_grid, 0)), 0)  # other diagonal


def check_reflection(input_grid):
    grid = np.array([[char for char in line] for line in input_grid])
    vertical = np.flip(grid, 1)
    horizontal = np.flip(grid, 0)
    if horizontal == grid or vertical == grid:
        return input_grid
    temp = find_offset(grid, horizontal)
    return temp if temp else find_offset(grid, vertical)


def find_offset(input_grid, altered_grid):  # not enforced, but intended
    # indexes get very confusing with two grids
    # for clarity we define x and y based on input_grid and only use that
    y, x = input_grid.shape
    # worst-case, every overlapping square is wrong
    minimum_bogie_ratio = 1
    # take the grid and try lining its top-left corner up with various points in flipped_grid
    for x_offset in range(x):
        for y_offset in range(y):
            grid_overlap = input_grid[x_offset:min(x, y + x_offset), y_offset:min(x + y_offset)]
            altered_overlap = altered_grid[0:min(y, x - x_offset), 0:min(x, y - y_offset)]
            bogie_count = np.count_nonzero(grid_overlap == altered_overlap)
            if bogie_count == 0:
                return x_offset, y_offset
            elif grid_overlap.size > 4:
                minimum_bogie_ratio = min(minimum_bogie_ratio, bogie_count/grid_overlap.size)
                # best_offset = x_offset, y_offset
                # up to 2 errors in a standard 15x15 grid (errors are doubled by reflection/rotation)
                if minimum_bogie_ratio < .02:
                    return grid_overlap
    return None
