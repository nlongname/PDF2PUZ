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


def build_puz(components, save_to=None, verbose=False):
    if not save_to:
        save_to = components['filename'] + '.puz'
        save_to = save_to.replace('cw', 'puz')
        print(save_to)
    output = bytearray(2)
    output.extend([ord(c) for c in 'ACROSS&DOWN\0'])
    output.extend(bytearray(10))  # this and the previous empty space are reserved for checksums
    output.extend(bytearray('1.3\0', encoding='windows-1252'))
    output.extend(bytearray(16))  # hard-coded this later
    output.extend([components['width'], components['length']])
    output.extend(components['num_clues'].to_bytes(2, 'little'))
    output.extend(b'\x01\x00\x00\x00')  # more magic numbers? plus more unused scramble

    partial_board = ''  # to calculate c_part later

    for line in components['grid']:
        output.extend(bytes(line, encoding='windows-1252'))
    for line in components['grid']:
        output.extend([45 + (c == '.') for c in line])  # empty grid, 45 for white squares, 46 for black
    for string in [components['title'], components['author'], components['copyright']]:
        output.extend(bytes(string + '\0', encoding='windows-1252'))  # .replace(b'\xc2\xa9', b'\xa9'))
        partial_board += (string + '\0')

    # clues

    across = components['clues']['across']
    down = components['clues']['down']

    for n in range(1, max(max(across), max(down)) + 1):
        if verbose:
            print(n)
        if n in across:
            output.extend(bytes(across[n] + '\0', encoding="windows-1252"))
            partial_board += across[n]
        if n in down:
            output.extend(bytes(down[n] + '\0', encoding="windows-1252"))
            partial_board += down[n]
    output.extend(bytes(components['notes'] + '\0', encoding="windows-1252"))
    if components['notes'] != '':
        partial_board += (components['notes'] + '\0')

    # GEXT (another empty grid for save data and circles)
    size = components['width'] * components['length']
    size_b = size.to_bytes(2, 'little')
    output.extend(bytes('GEXT', encoding="windows-1252") + size_b)
    checksum_index = len(output)
    output.extend(bytes(size + 3))  # 2 checksum + grid + 1 null terminator
    for i in components['circled']:
        output[checksum_index + 2 + i] = 0x80
    output[checksum_index:checksum_index + 2] = checksum(checksum_index + 2, size, 0, output)

    if components['rebuses'] != {}:
        # GRBS ("grid rebus", tells the rebus table which squares each rebus goes in)
        output.extend(bytes('GRBS', encoding="windows-1252") + size_b)
        checksum_index = len(output)
        output.extend(bytes(size + 3))
        rebuses = components['rebuses']
        rebus_table = sorted(list(rebuses.keys()), key=lambda x: min(rebuses[x]))
        for i, r in enumerate(rebus_table):
            for j in rebuses[r]:
                output[checksum_index + 2 + j] = i + 2  # one more than index, normally 1-indexed
        output[checksum_index:checksum_index + 2] = checksum(checksum_index + 2, size, 0, output)

        # RTBL ("rebus table", indexes each rebus square)
        output.extend(bytes('RTBL', encoding="windows-1252"))
        checksum_index = len(output)
        output.extend(bytes(4))
        for i, r in enumerate(rebus_table):
            output.extend(bytes(f"{' ' * (i < 10)}{i + 1}:{r};", encoding="windows-1252"))
        RTBL_len = len(output) - (checksum_index + 4)
        output.extend(b'\x00')
        output[checksum_index:checksum_index + 2] = RTBL_len.to_bytes(2, 'little')
        output[checksum_index + 2:checksum_index + 4] = checksum(checksum_index + 4, RTBL_len, 0, output)

    # various checksums
    c_cib = checksum(0x2C, 8, 0, output)
    c_soln = checksum(0x34, size, 0, output)
    c_gext = checksum(0x34 + size, size, 0, output)
    partial_board = bytearray(partial_board, encoding='windows-1252')
    c_part = checksum(0, len(partial_board), 0, partial_board)

    output[0x0E:0x10] = c_cib

    output[0x10] = 0x49 ^ c_cib[0]
    output[0x11] = 0x43 ^ c_soln[0]
    output[0x12] = 0x48 ^ c_gext[0]
    output[0x13] = 0x45 ^ c_part[0]

    output[0x14] = 0x41 ^ c_cib[1]
    output[0x15] = 0x54 ^ c_soln[1]
    output[0x16] = 0x45 ^ c_gext[1]
    output[0x17] = 0x44 ^ c_part[1]

    output[0x20:0x2C] = b'  RBJ III   '  # no idea what this is, but it seems to be consistent across NYT puzzles

    # "global" checksum
    temp = checksum(0x2c, 8 + size * 2, 0, output)
    output[:2] = checksum(0, len(partial_board), int.from_bytes(temp, byteorder="little"), partial_board)

    with open(save_to, 'wb') as file:  # note that 'save_to' includes the directory structure
        file.write(output)
    return (output, partial_board)