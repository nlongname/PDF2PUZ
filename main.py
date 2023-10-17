# Import libraries
# import pytesseract
# import sys
import os

from grid import *

full = True


def find_pdfs(filepath=None):
    if not filepath:
        filepath = os.getcwd()
    file_list = os.listdir(filepath)
    pdfs = []
    for file in file_list:
        name = file[:-4]
        extension = file[-4:]
        if extension == '.pdf':
            pdfs.append(name)
    return pdfs  # for now I won't include the folder, but I might need to


def grid_to_txt(name, grid):
    x_size = len(grid[0])
    y_size = len(grid)
    clue_numbers = get_clue_numbers(grid)
    across_len = len(clue_numbers['across'])
    down_len = len(clue_numbers['down'])
    with open(f'{name}_puz.txt', 'w') as f:
        f.write(
            f'<ACROSS PUZZLE V2>\n<TITLE>\n{name}\n<AUTHOR>\n\n<COPYRIGHT>\n\n<SIZE>\n{x_size}x{y_size}\n<GRID>\n')
        for line in grid:
            f.writelines(line)
            f.write('\n')
        f.write('<REBUS>\nMARK;\n<ACROSS>\n')
        f.write('-\n' * across_len)
        f.write('<DOWN>\n')
        f.write('-\n' * down_len)
        f.write('<NOTEPAD>\n')
    return
