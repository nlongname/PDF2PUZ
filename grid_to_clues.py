def get_clue_numbers(grid): 
	#grid expected to be a list of strings like 'XXXXX.XXXX.XXXX' 
	#where . indicates a black square
	down = []
	across = []
	number = 1
	increment_number=False
	for y in range(len(grid)):
		for x in range(len(grid[0])): #assumes it's a rectangle, not necessarily square
			if grid[y][x] != '.':
				if x==0 or (grid[y][x-1] == '.' and not (x == len(grid[0])-1 or grid[y][x+1] == '.')):
					#makes sure it's not a one-letter gap, since those don't get clued
					across.append(number)
					increment_number = True
				if y==0 or (grid[y-1][x] == '.' and not (y == len(grid)-1 or grid[y+1][x] == '.')):
					down.append(number)
					increment_number = True
			if increment_number:
				number += 1
				increment_number = False
	return {'across':across, 'down':down}


if __name__ == "__main__":
	test_grid = ['XXXXX.XXXX.XXXX',
				'XXXXX.XXXX.XXXX',
				'XXXXX.XXXX.XXXX',
				'..XXXXXXXXXXXXX',
				'...XXX...XXXXX.',
				'XXX.XXX.XXX.XXX',
				'XXXXXXXXXX.XXXX',
				'XXXXX.XXX.XXXXX',
				'XXXX.XXXXXXXXXX',
				'XXX.XXX.XXX.XXX',
				'.XXXXX...XXX...',
				'XXXXXXXXXXXXX..',
				'XXXX.XXXX.XXXXX',
				'XXXX.XXXX.XXXXX',
				'XXXX.XXXX.XXXXX']
	print(get_clue_numbers(test_grid))