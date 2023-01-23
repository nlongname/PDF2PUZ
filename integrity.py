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
    if np.all(rotated_grid == grid):
        return input_grid
    return find_offset(grid, rotated_grid)  # fixed grid or none


def check_diagonal(input_grid):
    grid = np.array([[char for char in line] for line in input_grid])
    flipped_grid = np.transpose(grid)
    if grid.shape == flipped_grid.shape and np.all(grid == flipped_grid):
        return input_grid
    temp = find_offset(grid, flipped_grid)
    if temp:
        return temp
    else:
        temp = find_offset(np.flip(grid, 0), np.flip(flipped_grid, 0))
        if temp:
            return np.flip(temp, 0)
        else:
            return None


def check_reflection(input_grid):
    grid = np.array([[char for char in line] for line in input_grid])
    vertical = np.flip(grid, 1)
    horizontal = np.flip(grid, 0)
    if np.all(horizontal == grid) or np.all(vertical == grid):
        return input_grid
    temp = find_offset(grid, horizontal)
    return temp if temp else find_offset(grid, vertical)


def find_offset(input_grid, altered_grid):  # not enforced, but intended
    iy, ix = input_grid.shape
    ay, ax = altered_grid.shape
    max_size = 0
    best_offset = None
    # take the altered grid and try lining its top-left corner up with various points in the input grid
    for x_offset in range(ix):
        for y_offset in range(iy):
            grid_overlap = input_grid[y_offset:min(iy, ay + y_offset), x_offset:min(ix, ax + x_offset)]
            altered_overlap = altered_grid[0:min(ay, iy - y_offset), 0:min(ax, ix - x_offset)]
            bogie_count = np.count_nonzero(grid_overlap != altered_overlap)
            bogie_ratio = bogie_count / grid_overlap.size
            if (x_offset, y_offset) == (0,1):
                print(bogie_ratio, grid_overlap.size)
            if bogie_ratio < .01:
                # 1 error in a standard 15x15 grid (remember, errors are doubled by reflection/rotation)
                # up to 2 in a 21x21 (Sunday-size) puzzle
                if grid_overlap.size > max_size:
                    max_size = grid_overlap.size
                    best_offset = (x_offset, y_offset)
    # This is basically a guess, might want to adjust it
    if max_size > .5*input_grid.size:
        return best_offset  # Not sure this is returning what I want it to either
    else:
        return None
