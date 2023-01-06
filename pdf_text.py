import PyPDF2
import re

def read(filename:str):
	#reads all data from PDF into one long string, replacing line breaks with spaces
	if filename[-4:] != '.pdf':
		filename = filename + '.pdf'
	f = open(filename, 'rb')
	reader = PyPDF2.PdfReader(f)
	page = reader.pages[0]
	raw = str(page.extract_text())
	f.close()
	#TODO: figure out what unsupported PDFs look like to fail to OCR
	return re.sub('\n', ' ', raw) 

def extract_clues(raw:str, clues:dict):
	down = clues['down']
	across = clues['across']
	print(raw)
	indices = [None]
	num=1
	numbers_at = {}
	while indices:
		indices = [i.start() for i in re.finditer(str(num), raw)]
		for i in indices:
			numbers_at[i] = numbers_at[i] + [num] if i in numbers_at else [num]
		num += 1
	to_delete = []
	for i in sorted(numbers_at.keys()):
		if len(numbers_at[i])>1:
			to_delete.append(i+1) #e.g. we find 2 and 23 at an index? we're going to find 3 at the next index
			numbers_at[i] = [max(numbers_at[i])] #and we want 23 not 2 here
	numbers_at = {k:v[0] for k,v in numbers_at.items() if k not in to_delete}
	indices = [(numbers_at[l], l) for l in sorted(numbers_at.keys())]
	streaks = []
	last_split = 0
	for i in range(1,len(indices)):
		if indices[i][0] < indices[i-1][0]:
			streaks.append(indices[last_split:i])
			last_split = i
	streaks.append(indices[last_split:len(indices)])

	while down not in streaks or across not in streaks:
		#TODO: figure out how to fix them if there's a number in a clue
		#concept: make a set starting at the beginning and adding up until
		# we have everything needed to make the set (excluding things accounted for)
		# then start from the last one we needed and go backwards to exclude
		# extra stuff at the beginning
		break

	for i,s in enumerate(streaks):
		temp_clues = [pair[0] for pair in s]
		next_index = len(raw) if i == len(streaks)-1 else streaks[i+1][0][1] #index of first part of next streak
		temp_indices = [pair[1] for pair in s] + [next_index]
		if temp_clues == down:
			down_clues = [raw[temp_indices[j]+len(str(temp_clues[j])):temp_indices[j+1]].strip() for j in range(len(temp_clues))]
		if temp_clues == across:
			across_clues = [raw[temp_indices[j]+len(str(temp_clues[j])):temp_indices[j+1]].strip() for j in range(len(temp_clues))]	
	print(down_clues)
	print(across_clues)




if __name__ == '__main__':
	extract_clues(read('L. A. Times, Tue, Jan 3, 2023'), {'across': [1, 6, 10, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 28, 30, 31, 33, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47, 49, 51, 56, 57, 58, 61, 62, 63, 64, 65, 66], 'down': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 22, 25, 26, 27, 29, 30, 32, 34, 35, 36, 39, 41, 42, 44, 48, 50, 51, 52, 53, 54, 55, 59, 60]})

['Pan Am rival', 'Roll of dough', 'Literary captain described as a "grand, ungodly, god- like man"', 'Casual rejections', 'Skated by, say', 'React to a yellow light, say', 'Indigenous language in Arizona', 'Touch borders with', "Slam-dancer's place", 'Emergency tire', 'Bite-sized treats whose name means "small ovens" in French', '"Honest!"', 'Spot for un chapeau', "Home brewer's ingredient", 'Domino indent', 'Up and about', 'Some hairy pets', 'Sweet Sixteen winners', 'Alphabetically ﬁrst noble gas', 'Mobile payment app', 'Fighting chance?', 'Director Spike', 'Fair-hiring initials', 'Spree', 'Pay, reluctantly', 'Soccer star and equal-pay advocate Megan', "Donkey's need, in a party game", 'Future flower', 'Overjoy', 'Common lab culture', "Paul Bunyan's blue ox", 'Feeling nothing', 'Smooth-talking', 'Nonkosher sammies', "Potter's oven", 'Jar topper', 'Donkey']
['Country music sound', 'Coordinating pillowcase', 'Roasting rod', '"Yippee!"', 'Basketball commentator Rebecca', 'Long-haired lap dog, familiarly', 'Change with the times', 'Major composition', 'Working hard', "Smile broadly because of one's own achievement, say", 'Place for a scrub', 'Devoutness', 'Grabbed a bite', 'Chicken __ king', 'Red carpet walker', 'Electric key', "New York City district that's home to the Fearless Girl statue", 'Soup du __', 'Sign of spring', 'Lead-in to Z or Alpha', 'Koalas and emus, in Australia', 'Novelist Atkinson', "Desirable feature of kids' clothing", 'WSW oppositeDOWN', 'Prohibit', 'Rowboat need', 'Cap letters at Busch Stadium', 'Get ready to drive?', 'Mike and __: fruit- flavored candy', 'Amino acid, vis-à-vis protein', 'Aquarium growth', "Void's partner", '"Ta-da!"', 'Thai currency', 'Leave out', '"Black-ish" star Tracee __ Ross', 'East, in Spanish', 'Recedes', 'Pomelo peels']