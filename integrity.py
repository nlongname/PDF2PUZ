# Testing whether a generated grid meets general integrity standards
# probably including desired size

# Tests, from easy to hard:
# no outer edges should be all black (all '.')
# outer edges shouldn't be all blank (all 'X') unless the shape dictates it
# symmetry (usually rotational, but sometimes diagonal or vertical or horizontal)
# if it's a little off, what do you do? (multiple clue lists? ask user?)

import numpy as np


def area(rect):
    if rect == None:
        return 0
    else:
        return len(rect)*len(rect[0])


def clean_edges(input_grid, target_size=(15, 15)):
    if not input_grid:
        return None
    grid = np.array([[char for char in line] for line in input_grid])
    if grid.shape == target_size:
        grid = [''.join(line) for line in grid]  # just in case it's in the pre-split format, still works if it's not
        return grid
    not_done = True
    lines_removed = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # for debugging now, but might use it later
    while not_done:  # clear all-black lines first
        not_done = False
        if np.all(grid[:, 0] == '.'):
            lines_removed['left'] += 1
            grid = grid[:, 1:]
            not_done = True
        if np.all(grid[:, -1] == '.'):
            lines_removed['right'] += 1
            grid = grid[:, :-1]
            not_done = True
        if np.all(grid[0, :] == '.'):
            lines_removed['top'] += 1
            grid = grid[1:, :]
            not_done = True
        if np.all(grid[-1, :] == '.'):
            lines_removed['bottom'] += 1
            grid = grid[:-1, :]
            not_done = True
    not_done = True
    while not_done:  # then all-white lines
        # doing all-white separately and after all-black works better for small, sparse puzzles like NYT Minis
        not_done = False
        if not np.any(grid[:, 0] == '.'):
            lines_removed['left'] += 1
            grid = grid[:, 1:]
            not_done = True
        if not np.any(grid[:, -1] == '.'):
            lines_removed['right'] += 1
            grid = grid[:, :-1]
            not_done = True
        if not np.any(grid[0, :] == '.'):
            lines_removed['top'] += 1
            grid = grid[1:, :]
            not_done = True
        if not np.any(grid[-1, :] == '.'):
            lines_removed['bottom'] += 1
            grid = grid[:-1, :]
            not_done = True
    # if grid.shape == target_size:
    #     lines_removed = None
    grid = [''.join(line) for line in grid]
    return grid


def check_rotational(input_grid):
    grid = np.array([[char for char in line] for line in input_grid])
    rotated_grid = np.rot90(grid, 2)
    if np.all(rotated_grid == grid):
        return input_grid
    return find_offsets(grid, rotated_grid)  # fixed grid or none


def check_diagonals(input_grid):
    grid = input_grid
    flipped_grid = input_grid[::-1]
    diag = check_diagonal(grid)
    flipped_diag = check_diagonal(flipped_grid)
    if flipped_diag:
        flipped_diag = flipped_diag[::-1]
    return diag if area(diag) > area(flipped_diag) else flipped_diag


def check_diagonal(input_grid):
    grid = np.array([[char for char in line] for line in input_grid])
    diagonal_grid = np.transpose(grid)
    if grid.shape == diagonal_grid.shape and np.all(grid == diagonal_grid):
        return input_grid
    return find_offsets(grid, diagonal_grid)


def check_reflection(input_grid):
    grid = np.array([[char for char in line] for line in input_grid])
    vertical = np.flip(grid, 1)
    horizontal = np.flip(grid, 0)
    if np.all(horizontal == grid) or np.all(vertical == grid):
        return input_grid
    horiz = find_offsets(grid, horizontal)
    vert = find_offsets(grid, vertical)
    return horiz if area(horiz) > area(vert) else vert


def find_offsets(input_grid, altered_grid):
    first_try = find_offset(input_grid, altered_grid, focus_left=True)
    second_try = find_offset(altered_grid, input_grid, focus_left=False)
    return first_try if area(first_try) > area(second_try) else second_try


def find_offset(left_grid, right_grid, focus_left:bool):
    iy, ix = left_grid.shape
    ay, ax = right_grid.shape
    max_size = 0
    best_grid = None
    # take the altered grid and try lining its top-left corner up with various points in the input grid
    # accuracies = np.empty((iy, ix))
    for x_offset in range(ix):
        for y_offset in range(iy):
            left_overlap = left_grid[y_offset:min(iy, ay + y_offset), x_offset:min(ix, ax + x_offset)]
            right_overlap = right_grid[0:min(ay, iy - y_offset), 0:min(ax, ix - x_offset)]
            bogie_count = np.count_nonzero(left_overlap != right_overlap)
            bogie_ratio = bogie_count / left_overlap.size
            # accuracies[y_offset,x_offset] = bogie_ratio
            if bogie_ratio < .01:
                # 1 error in a standard 15x15 grid (remember, errors are doubled by reflection/rotation)
                # up to 2 in a 21x21 (Sunday-size) puzzle
                if left_overlap.size > max_size:
                    # print("good one", left_overlap.size)
                    # best_offset = (x_offset, y_offset)
                    max_size = left_overlap.size
                    if focus_left:
                        best_grid = [''.join(line) for line in left_overlap]
                    else:
                        best_grid = [''.join(line) for line in right_overlap]
    # This .5 is basically a guess, might want to adjust it
    # TODO: better way of determining area of overlap to eliminate bogies on all sides;
    #  maybe something recursive? knock off two sides then go back for the other two
    # print(accuracies)
    if max_size > .5*left_grid.size:
        return best_grid
    else:
        return None

def check_symmetries(grid, target_size = (15, 15)):
    cleaned_grid = clean_edges(grid, target_size)
    best_symmetry = max([check_rotational(cleaned_grid), check_diagonals(cleaned_grid), check_reflection(cleaned_grid)], key=area)
    return best_symmetry