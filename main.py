# Import libraries
from PIL import Image
#import pytesseract
#import sys
from pdf2image import convert_from_path
import os
import numpy as np
import pprint as pp

full = True

file_list = os.listdir()
for pdf in file_list:
    name = pdf[:-4]
    if pdf[-4:] == ".pdf" and (full == True or f"{name}.jpg" not in file_list):
        print(name)
        pic = convert_from_path(pdf, dpi=36, fmt="jpg")[0]
        # TODO: dynamically change DPI. 200 works the best (but breaks on supermega), 50 is way faster but leaves artifacts (DICT, supermega)
        pic.save(f"{name}.jpg", 'JPEG')
        # OCR for clues
        #        outfile = f"{name}.txt"
        #        f = open(outfile, "w")
        #        text = pytesseract.image_to_string(f"{name}.jpg")
        #        f.write(text)
        #        f.close()

        # isolate black squares in grid
        pix = Image.open(f"{name}.jpg")
        pix = np.asarray(pix)
        black = set()
        a = 3
        coords = {}
        new = set()
        ranges = {y: [] for y in range(pic.size[1])}
        for y in range(pic.size[1]):
            streak = 0
            for x in range(pic.size[0]):
                if sum(pix[y, x]) <= 255 * 3 / 2:
                    black.add((y, x))
                    streak += 1
                else:
                    if streak > 2 * a:
                        ranges[y].append((x - streak, x - 1))
                    streak = 0
        ranges = {r: ranges[r] for r in ranges if ranges[r] != []}

        # can I get away without this part by only taking "streaks" longer than 2a?
        # I'll have to do a different post-processing to make sure it's long enough
        # in the other direction

        #        for (y, x) in black:
        #            if (max(0, y-a), max(0,x-a)) in black and (y, max(0,x-a)) in black and (min(y+a,pic.size[1]),max(0,x-a)) in black and (max(y-a,0),x) in black and (min(y+a,pic.size[1]),x) in black and (max(y-a,0),min(x+a,pic.size[0])) in black and (y,min(x+a,pic.size[0])) in black and (min(y+a,pic.size[1]),min(x+a,pic.size[0])) in black:
        #                    new.add((y, x))

        # not going to deal with recreating a visible map for now

        # process coordinates to try to find grid lines

        #        ranges = {x:[] for x in coords}
        #        for x in range(pix.size[0]):
        #            ys = coords[x]
        #            while len(ys) > 0:
        #                i = ys[0]
        #                j = 1
        #                while i+j in ys:
        #                    j += 1
        #                if j > 5 :
        #                    ranges[x].append((i-a, i+j-1+a)) #best estimate to get edges back to where they started
        #                    #w = j-1+2*a
        #                    #if w in widths:
        #                    #    widths[w] += 1
        #                    #else:
        #                    #    widths[w]=1
        #                ys = ys[j:]

        widths = {}
        for y in ranges:
            r = ranges[y]
            for i in r:
                for j in r:
                    if i != j:
                        u = abs(i[0] - j[0])
                        v = abs(i[1] - j[1])
                        widths[u] = widths[u] + 1 if u in widths else 1
                        widths[v] = widths[v] + 1 if v in widths else 1
        # print(widths)
        widths = {y: widths[y] for y in widths if widths[y] > sum(widths.values()) / 100}
        # print(widths)
        widths = sorted(widths.keys())
        # I think this initial guess is the core problem that's leading to chaotic outcomes for different DPI/a-values
        # TODO: make initial guess based on domain knowledge of crosswords, not presumably-messy data
        guess = min([widths[i + 1] - widths[i] for i in range(len(widths) - 1) if
                     widths[i + 1] - widths[i] > 2 * a])  # not sure about this 2*a
        boxes = {}
        working = True
        i = 0
        previous_guess = 0
        while i < len(widths):
            b = widths[i] / guess
            if abs(b - round(b)) <= .2:
                if round(b) in boxes:
                    boxes[round(b)] += [widths[i]]
                else:
                    boxes[round(b)] = [widths[i]]
            else:
                working = False
            i += 1
            if i == 1:
                guess = widths[0] / round(widths[0] / guess)
            else:
                temp = [sum(boxes[y]) / len(boxes[y]) / y for y in boxes.keys()]
                guess = sum(temp) / len(temp)
                print(guess)
                if guess != previous_guess:
                    previous_guess = guess
                else:
                    break
            if not working:
                i = 0
                working = True
        ranges = {y: ranges[y] for y in ranges if ranges[y] != []}
        for r in ranges:
            temp = []
            for d in ranges[r]:
                l = d[1] - d[0]
                if l > guess * .75 and abs(l / guess - round(l / guess)) < .2:
                    temp.append(d)
            ranges[r] = temp
        ranges = {y: ranges[y] for y in ranges if ranges[y] != []}
        # check y-streaks
        streak = 0
        y_streaks = []
        to_keep = []
        for y in range(pic.size[1]):
            if y in ranges:
                streak += 1
            else:
                if streak > 2 * a:
                    y_streaks.append((y - streak, y - 1))
                    for past_y in range(y - streak, y):
                        to_keep.append(past_y)
                streak = 0
        ranges = {k: v for k, v in ranges.items() if k in to_keep}

        # the .5's are to get the centers of the squares
        left = min(ranges)
        baseline = ranges[round(left + guess * .5)][0][0]  # this will break if there's a bogie on the left side
        black_squares = set()
        black_square_counts = {}
        for i in range(round((max(ranges) - left) / guess)):
            y = round(left + guess * (i + .5))
            if y in ranges:
                for d in ranges[y]:
                    for j in range(round((d[0] - baseline) / guess), round((d[1] - baseline) / guess)):
                        black_squares.add((i, j))
                        black_square_counts[(i, j)] = black_square_counts[(i, j)] + 1 if (i,
                                                                                          j) in black_square_counts else 1
        offset = -min(black_squares, key=lambda y: y[1])[1]
        black_squares = {(y[0], y[1] + offset) for y in black_squares}
        x_size = max(black_squares, key=lambda x: x[0])[0] + 1
        y_size = max(black_squares, key=lambda x: x[1])[1] + 1

        # TODO: check if full rows or columns are all dots, which seems to happen at low DPI; if so remove them and re-do sizes

        print(x_size, y_size)
        print(black_squares)

        template = ['X' * x_size for y in range(y_size)]
        for bs in black_squares:
            template[bs[1]] = template[bs[1]][:bs[0]] + '.' + template[bs[1]][bs[0] + 1:]
        pp.pprint(template)

        # words will be in the form '...XXX...XXX...XXX...', so every '.X' indicates a new word
        # with an extra word if the first character is a letter rather than '.'
        # note: I am not generating a solution so all letters are coded 'x' or 'X'
        down = sum(l.count('.x') + l.count('.X') + (1 if l[0] != '.' else 0) for l in template)

        transpose = ['X' * y_size for y in range(x_size)]
        for bs in black_squares:
            transpose[bs[0]] = transpose[bs[0]][:bs[1]] + '.' + transpose[bs[0]][bs[1] + 1:]
        across = sum(l.count('.x') + l.count('.X') + (1 if l[0] != '.' else 0) for l in transpose)
        pp.pprint(transpose)

        with open(f'{name}_puz.txt', 'w') as f:
            f.write(
                f'<ACROSS PUZZLE V2>\n<TITLE>\n{name}\n<AUTHOR>\n\n<COPYRIGHT>\n\n<SIZE>\n{x_size}x{y_size}\n<GRID>\n')
            for line in transpose:
                f.writelines(line)
                f.write('\n')
            f.write('<REBUS>\nMARK;\n<ACROSS>\n')
            f.write('-\n' * across)
            f.write('<DOWN>\n')
            f.write('-\n' * down)
            f.write('<NOTEPAD>\n')
