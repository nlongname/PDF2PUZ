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

def extract_clues(raw:str):
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
	indices = sorted(numbers_at.keys())
	clue_numbers = [numbers_at[l] for l in indices]
	streaks = []
	last_split = 0
	for i in range(1,len(clue_numbers)):
		if clue_numbers[i] < clue_numbers[i-1]:
			streaks.append(clue_numbers[last_split:i])
			last_split = i
	streaks.append(clue_numbers[last_split:len(clue_numbers)])
	streaks = [s for s in streaks if len(s) != s[-1]]
	print(streaks)




if __name__ == '__main__':
	extract_clues(read('LAT'))