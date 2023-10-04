import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import pprint as pp
from math import sqrt


def luminance(pixel):
	r, g, b = pixel
	return 0.2126 * r + 0.7152 * g + 0.0722 * b


def grid_from_pdf(filename, gridsize=(15, 15)):
	if filename[-4:] == '.pdf':
		filename = filename[:-4]
	dpi = 200
	pic = convert_from_path(filename, dpi=dpi, fmt="png")[0]  # hopefully PNG will be more consistent than JPG
	# TODO: dynamically change DPI. 200 works the best (but breaks on supermega),
	#  50 is way faster but leaves artifacts (DICT, for example)
	pic.save(f"{filename}.png", 'PNG')
	# OCR for clues
	#        outfile = f"{name}.txt"
	#        f = open(outfile, "w")
	#        text = pytesseract.image_to_string(f"{name}.jpg")
	#        f.write(text)
	#        f.close()
	return grid_from_pic(f"{filename}.png", gridsize, dpi)


def grid_from_pic(filename, gridsize=(15, 15), dpi=200):
	# TODO: debug/refactor  this split when I can actually use pdf2image

	pic = Image.open(filename)
	pixel_array = np.array([[luminance(p) for p in q] for q in np.array(pic)])

	luminance_cutoff = 100  # TODO: make this dynamic, maybe based on "black" pixel count?

	test_array = np.array([[[255, 255, 255] if p > luminance_cutoff else [0, 0, 0] for p in q]
						   for q in pixel_array], dtype='uint8')
	test_image = Image.fromarray(test_array)
	test_image.show()

	black = set()
	a = round(5*sqrt(dpi/50))  # TODO: make a more descriptive name and make it parametric
	# I think this initial guess is the core problem that's leading to chaotic outcomes for different DPI/a-values
	# TODO: use initial guess based on domain knowledge of crosswords, not presumably-messy data
	ranges = {y: [] for y in range(pic.size[1])}
	# isolate black squares in grid
	for y in range(pic.size[1]):
		streak = 0
		for x in range(pic.size[0]):
			if pixel_array[y, x] < luminance_cutoff:
				black.add((y, x))
				streak += 1
			else:
				if streak > 2*a:
					ranges[y].append((x - streak, x - 1))
				streak = 0
	ranges = {r: ranges[r] for r in ranges if ranges[r] != []}
	print(ranges)

	# process coordinates to try to find grid

	widths = {}
	for y in ranges:
		r = ranges[y]
		for i in r:
			w = abs(i[1]-i[0])
			widths[w] = widths[w] + 2 if w in widths else 2  # later process double-counts, so we double here too
			for j in r:
				if i != j:
					u = abs(i[0] - j[0])
					v = abs(i[1] - j[1])
					widths[u] = widths[u] + 1 if u in widths else 1
					widths[v] = widths[v] + 1 if v in widths else 1
	print(widths)
	cutoff = sum(widths.values()) / 100
	widths = {y: widths[y] for y in widths if widths[y] > cutoff}  # eliminate outliers
	# best = [w for w in widths if widths[w] == max(widths.values())]
	widths = sorted(widths.keys())
	print(widths)
	print(pic.size, dpi, gridsize)

	# guess = sum(best)/len(best)

	guess = round(.5 * (pic.size[1] / 3 / gridsize[1] + pic.size[0] / 2.3 / gridsize[0]))
	print(guess)
	# guess = min([widths[i + 1] - widths[i] for i in range(len(widths) - 1) if
	#              widths[i + 1] - widths[i] > 2 * a])  # not sure about this 2*a
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
	print(ranges)
	for r in ranges:
		temp = []
		for d in ranges[r]:
			length = d[1] - d[0]
			if length > guess * .75 and abs(length / guess - round(length / guess)) < .2:
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
	print(ranges)

	# the .5's are to get the centers of the squares
	left = min(ranges.values())[0][0]
	print(left)
	right = max(ranges.values(), key=lambda r: r[-1][-1])[-1][-1]
	print(right)
	full_lines = [k for k in ranges if ranges[k] == [(left, right)]]
	len_before = 0
	len_after = len(full_lines)
	# this full-line method works very well on certain files, but fails completely on many others
	# might be useful as a backup method later on
	while len_before != len_after:
		full_lines = [l for l in full_lines if l+1 not in full_lines]
		len_before = len_after
		len_after = len(full_lines)
	y_size = len_after - 1

	black_squares = set()
	for i in range(y_size):
		y = full_lines[i]+1
		for d in ranges[y]:
			print(d, (round((d[0]-left)/guess), round((d[1]-left)/guess)))
			for j in range(round((d[0] - left) / guess), round((d[1] - left) / guess)):
				black_squares.add((i, j))
	x_size = max(black_squares, key=lambda z: z[0])[0] + 1  # TODO: adjust size and redo if sizes are close but wrong?
	# y_size = max(black_squares, key=lambda z: z[1])[1] + 1

	print(x_size, y_size)
	print(black_squares)
	# TODO: clean this up, really shouldn't need to transpose at all
	template = ['X' * x_size for _ in range(y_size)]
	for bs in black_squares:
		template[bs[1]] = template[bs[1]][:bs[0]] + '.' + template[bs[1]][bs[0] + 1:]
	pp.pprint(template)

	# words will be in the form '...XXX...XXX...XXX...', so every '.X' indicates a new word
	# with an extra word if the first character is a letter rather than '.'
	# note: I am not generating a solution so all letters are coded 'x' or 'X'

	# down = sum(l.count('.x') + l.count('.X') + (1 if l[0] != '.' else 0) for l in template)

	transpose = ['X' * y_size for _ in range(x_size)]
	for bs in black_squares:
		transpose[bs[0]] = transpose[bs[0]][:bs[1]] + '.' + transpose[bs[0]][bs[1] + 1:]
	# across = sum(l.count('.x') + l.count('.X') + (1 if l[0] != '.' else 0) for l in transpose)
	# pp.pprint(transpose)
	# TODO: crossword-specific integrity check: check symmetry, check size compared to expected, etc.
	# (possibly combined) check if full rows or columns are all dots, which seems to happen at low DPI;
	# if so remove them and re-do sizes
	# probably separate these each out so it's easy to re-do the square-size guess if it's not fixable
	return transpose


def get_clue_numbers(grid):
	# grid expected to be a list of strings like 'XXXXX.XXXX.XXXX'
	# where . indicates a black square
	down = []
	across = []
	number = 1
	increment_number = False
	for y in range(len(grid)):
		for x in range(len(grid[0])):  # assumes it's a rectangle, not necessarily square
			if grid[y][x] != '.':
				if (x == 0 and grid[y][1] != '.') or (grid[y][x-1] == '.' and not (x == len(grid[0])-1 or grid[y][x+1] == '.')):
					# makes sure it's not a one-letter gap, since those don't get clued
					across.append(number)
					increment_number = True
				if (y == 0 and grid[1][x] != '.') or (grid[y-1][x] == '.' and not (y == len(grid)-1 or grid[y+1][x] == '.')):
					down.append(number)
					increment_number = True
			if increment_number:
				number += 1
				increment_number = False
	return {'across': across, 'down': down}
