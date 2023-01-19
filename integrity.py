# Testing whether a generated grid meets general integrity standards
# probably including desired size

# Tests, from easy to hard:
# no outer edges should be all black (all '.')
# outer edges shouldn't be all blank (all 'X') unless the shape dictates it
# symmetry (usually rotational, but sometimes diagonal or vertical or horizontal)
# if it's a little off', what do you do? (multiple clue lists? ask user?)

import numpy as np

def clean_edges(input_grid, size = (15,15)):
    grid = np.array([[char for char in line] for line in input_grid])
    if grid.shape == size:
        grid = [''.join(line) for line in grid] # just in case it's in the pre-split format, still works if it's not
        return (grid, None)
    not_done = True
    while not_done: # clear all-black lines first
        not_done = False
        if np.all(grid[:, 0]=='.'):
            grid = grid[:,1:]
            not_done = True
        if np.all(grid[:, -1]=='.'):
            grid = grid[:,:-1]
            not_done = True
        if np.all(grid[0, :]=='.'):
            grid = grid[1:, :]
            not_done = True
        if np.all(grid[-1, :]=='.'):
            grid = grid[:-1, :]
            not_done = True
    blanks_removed = {'left':0, 'right':0, 'top':0, 'bottom':0} # for debugging now, but might use it later
    not_done = True
    while not_done: # then all-white lines
        # doing all-white separately and after all-black works better for small, sparse puzzles like NYT Minis
        not_done = False
        if not np.any(grid[:, 0]=='.'):
            blanks_removed['left'] += 1
            grid = grid[:,1:]
            not_done = True
        if not np.any(grid[:, -1]=='.'):
            blanks_removed['right'] += 1
            grid = grid[:,:-1]
            not_done = True
        if not np.any(grid[0, :]=='.'):
            blanks_removed['top'] += 1
            grid = grid[1:, :]
            not_done = True
        if not np.any(grid[-1, :]=='.'):
            blanks_removed['bottom'] += 1
            grid = grid[:-1, :]
            not_done = True
    if grid.shape != size:
        blanks_removed = None
    grid = [''.join(line) for line in grid]
    return (grid, blanks_removed)

def check_rotational(input_grid):
    grid = np.array([[char for char in line] for line in input_grid])
    flipped_grid = np.rot90(grid, 2)
    if flipped_grid == grid:
        return input_grid
