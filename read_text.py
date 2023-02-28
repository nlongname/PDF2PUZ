import PyPDF2
import re


def read(filename: str):
	# reads all text from PDF into one long string, replacing line breaks with spaces
	if filename[-4:] != '.pdf':
		filename = filename + '.pdf'
	f = open(filename, 'rb')
	reader = PyPDF2.PdfReader(f)
	page = reader.pages[0]
	raw = str(page.extract_text())
	f.close()
	# TODO: figure out what unsupported PDFs look like to fail to OCR
	return re.sub('\n', ' ', raw)
	# what if I didn't do this, and used the line break as an indicator when there are duplicate numbers?


def extract_clues(raw: str, clues: dict):
	#print(raw)
	indices = [None]
	num = 1
	numbers_at = {}
	while indices:
		indices = [i.start() for i in re.finditer(str(num), raw)]
		for i in indices:
			numbers_at[i] = numbers_at[i] + [num] if i in numbers_at else [num]
		num += 1
	to_delete = []
	for i in sorted(numbers_at.keys()):
		if len(numbers_at[i]) > 1:
			to_delete.append(i+1)  # e.g. we find 2 and 23 at an index? we're going to find 3 at the next index
			numbers_at[i] = [max(numbers_at[i])]  # and we want 23 not 2 here
	numbers_at = {k: v[0] for k, v in numbers_at.items() if k not in to_delete}
	indices = [(numbers_at[m], m) for m in sorted(numbers_at.keys())]
	streaks = []
	last_split = 0
	for i in range(1, len(indices)):
		if indices[i][0] < indices[i-1][0]:
			streaks.append(indices[last_split:i])
			last_split = i
	streaks.append(indices[last_split:len(indices)])

	streaks = [streak if len(streak) != streak[-1][0] else [streak[0], streak[-1]] for streak in streaks]

	# concept: make a set starting at the beginning and adding up until
	# we have everything needed to make the set (excluding things accounted for)
	# then start from the last one we needed and go backwards to exclude
	# extra stuff at the beginning
	for name in ['down', 'across']:
		cumulative_list = []
		cumulative_set = set()
		target_set = set(clues[name])
		i = 0
		# this might accumulate extra elements, but we keep going until we have the whole target set
		while i < len(streaks) and target_set - cumulative_set != set():
			cumulative_set.update([s[0] for s in streaks[i]])
			i += 1
		if i == len(streaks):
			#raise Exception("target set not found")
			return None
		max_index = i
		i -= 1
		cumulative_set = set()
		while target_set - cumulative_set != set():
			cumulative_list = streaks[i] + cumulative_list
			cumulative_set.update([s[0] for s in streaks[i]])
			i -= 1
		min_index = i+1
		if min_index != max_index-1:
			cumulative_list = [pair for pair in cumulative_list if pair[0] in clues[name]]
			while True:
				bogies = []
				for j in range(len(cumulative_list)):
					try:
						if j == 0:
							if cumulative_list[0][0] != clues[name][0]:
								bogies.append(0)
						elif j == len(cumulative_list)-1:
							if cumulative_list[-1][0] != clues[name][-1]:
								bogies.append(j)
						elif clues[name][clues[name].index(cumulative_list[j][0])-1] not in [pair[0] for pair in cumulative_list[:j]] \
							or clues[name][clues[name].index(cumulative_list[j][0])+1] not in [pair[0] for pair in cumulative_list[j+1:]]:
							bogies.append(j)
					except(IndexError):
						break
				if not bogies:
					break
				cumulative_list = [pair for i, pair in enumerate(cumulative_list) if i not in bogies]
		if len(cumulative_list) > len(clues[name]):
			candidates = [pair for pair in cumulative_list if len([p for p in cumulative_list if p[0] == pair[0]]) > 1]
			endings = ["st,", "st ", "st.", "st-", "nd,", "nd ", "nd.", "nd-", "th,", "th ", "th.", "th-"]
			bogies = [pair[1] for pair in candidates if raw[pair[1]+len(str(pair[0])):pair[1]+len(str(pair[0]))+3] in endings]
			if len(bogies) <= len(cumulative_list)-len(clues[name]):
				cumulative_list = [pair for pair in cumulative_list if pair[1] not in bogies]
				candidates = [candidate for candidate in candidates if candidate[1] not in bogies]
			endings = ["\"", "-", ")", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
			bogies = [pair[1] for pair in candidates if raw[pair[1]+len(str(pair[0])):pair[1]+len(str(pair[0]))+1] in endings]
			if len(bogies) <= len(cumulative_list)-len(clues[name]):
				cumulative_list = [pair for pair in cumulative_list if pair[1] not in bogies]
				candidates = [candidate for candidate in candidates if candidate[1] not in bogies]
			bogies = [pair[1] for pair in candidates if raw[pair[1]-1:pair[1]] in endings]
			if len(bogies) <= len(cumulative_list)-len(clues[name]):
				cumulative_list = [pair for pair in cumulative_list if pair[1] not in bogies]
		# TODO: make some kind of final safeguard, if nothing else works just take a guess?
		# maybe use the average clue length to see which clue lengths make more sense
		streaks[min_index:max_index] = [cumulative_list]
	
	for i, s in enumerate(streaks):
		temp_clues = [pair[0] for pair in s]
		next_index = len(raw) if i == len(streaks)-1 else streaks[i+1][0][1]  # index of first part of next streak
		temp_indices = [pair[1] for pair in s] + [next_index]
		if temp_clues == clues['down']:
			down_clues = [raw[temp_indices[j]+len(str(temp_clues[j])):temp_indices[j+1]].strip() for j in range(len(temp_clues))]
		if temp_clues == clues['across']:
			across_clues = [raw[temp_indices[j]+len(str(temp_clues[j])):temp_indices[j+1]].strip() for j in range(len(temp_clues))]
	try:
		return {'down': down_clues, 'across': across_clues}
	except UnboundLocalError:
		return None


if __name__ == '__main__':
	print(extract_clues(read('L. A. Times, Tue, Jan 3, 2023'),
							{'across': [1, 6, 10, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 28, 30, 31, 33, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47, 49, 51, 56, 57, 58, 61, 62, 63, 64, 65, 66],
							'down': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 22, 25, 26, 27, 29, 30, 32, 34, 35, 36, 39, 41, 42, 44, 48, 50, 51, 52, 53, 54, 55, 59, 60]}))
	# ['Pan Am rival', 'Roll of dough', 'Literary captain described as a "grand, ungodly, god- like man"', 'Casual rejections', 'Skated by, say', 'React to a yellow light, say', 'Indigenous language in Arizona', 'Touch borders with', "Slam-dancer's place", 'Emergency tire', 'Bite-sized treats whose name means "small ovens" in French', '"Honest!"', 'Spot for un chapeau', "Home brewer's ingredient", 'Domino indent', 'Up and about', 'Some hairy pets', 'Sweet Sixteen winners', 'Alphabetically ﬁrst noble gas', 'Mobile payment app', 'Fighting chance?', 'Director Spike', 'Fair-hiring initials', 'Spree', 'Pay, reluctantly', 'Soccer star and equal-pay advocate Megan', "Donkey's need, in a party game", 'Future flower', 'Overjoy', 'Common lab culture', "Paul Bunyan's blue ox", 'Feeling nothing', 'Smooth-talking', 'Nonkosher sammies', "Potter's oven", 'Jar topper', 'Donkey']
	# ['Country music sound', 'Coordinating pillowcase', 'Roasting rod', '"Yippee!"', 'Basketball commentator Rebecca', 'Long-haired lap dog, familiarly', 'Change with the times', 'Major composition', 'Working hard', "Smile broadly because of one's own achievement, say", 'Place for a scrub', 'Devoutness', 'Grabbed a bite', 'Chicken __ king', 'Red carpet walker', 'Electric key', "New York City district that's home to the Fearless Girl statue", 'Soup du __', 'Sign of spring', 'Lead-in to Z or Alpha', 'Koalas and emus, in Australia', 'Novelist Atkinson', "Desirable feature of kids' clothing", 'WSW oppositeDOWN', 'Prohibit', 'Rowboat need', 'Cap letters at Busch Stadium', 'Get ready to drive?', 'Mike and __: fruit- flavored candy', 'Amino acid, vis-à-vis protein', 'Aquarium growth', "Void's partner", '"Ta-da!"', 'Thai currency', 'Leave out', '"Black-ish" star Tracee __ Ross', 'East, in Spanish', 'Recedes', 'Pomelo peels']
	modified_raw = "1/6/23, 5:40 AM L. A. Times, Tue, Jan 3, 2023 https://cdn4.amuselabs.com/lat/crossword-pdf 1/1L. A. Times, Tue, Jan 3, 2023 By Rebecca Goldstein / Ed. Patti Varol © 2023 Tribune Content Agency, LLC ACROSS 1Country music sound for R2-D2 6Coordinating pillowcase 10Roasting rod 14\"Yippee!\" 151992 Basketball commentator Rebecca 16Long-haired lap dog, familiarly 17Change with the times 18Major 1920 composition 19Working hard 20Smile broadly because of one's own achievement, say 23 Place for a scrub 24Devoutness 25 Grabbed a bite 28 Chicken __ king 30Red carpet walker 31Electric key 33New York City district that's home to the Fearless Girl statue 36Soup du __ 37Sign of spring 38Lead-in to Z or Alpha 39Koalas and emus, in Australia 40Novelist Atkinson 41Desirable feature of kids' clothing 43WSW oppositeDOWN44Prohibit 45Rowboat need 46Cap letters at Busch Stadium 47Get ready to drive? 49Mike and __: fruit- flavored candy 51Amino acid, vis-à-vis protein 56Aquarium growth 57Void's partner 58\"Ta-da!\" 61Thai currency 62Leave out 63\"Black-ish\" star Tracee __ Ross 64East, in Spanish 65Recedes 66Pomelo peels 1Pan Am (and R2-D2) rival 2Roll of dough 3Literary captain described as a \"grand, ungodly, god- like man\" 4Casual rejections 5Skated by, say 6React to a yellow light, say 7Indigenous language in Arizona 8Touch borders with 9Slam-dancer's place 10Emergency tire11Bite-sized treats whose name means \"small ovens\" in French 12\"Honest!\" 13Spot for un 21st-century chapeau 21Home brewer's ingredient 22 Domino indent 25 Up and about 26 Some hairy pets 27Sweet Sixteen winners29 Alphabetically ﬁrst noble gas 30Mobile payment app 32Fighting chance? 34Director Spike 35Fair-hiring initials 36Spree 39Pay, reluctantly 41Soccer star and equal-pay advocate Megan42Donkey's need, in a party game 44Future flower 48Overjoy 50Common lab culture 51Paul Bunyan's blue ox 52Feeling nothing 53Smooth-talking 54Nonkosher sammies 55Potter's oven 59Jar topper 60Donkey1 2 3 4 5   6 7 8 9   10 11 12 13  14   15   16  17   18   19  20 21 22  23   24  25 26 27   28 29   30   31 32  33 34 35   36  37   38   39  40   41 42  43   44   45   46  47 48   49 50  51 52 53 54 55  56   57   58 59 60  61   62   63  64   65   66 "
	extract_clues(modified_raw, {'across': [1, 6, 10, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 28, 30, 31, 33, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47, 49, 51, 56, 57, 58, 61, 62, 63, 64, 65, 66], 'down': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 22, 25, 26, 27, 29, 30, 32, 34, 35, 36, 39, 41, 42, 44, 48, 50, 51, 52, 53, 54, 55, 59, 60]})
