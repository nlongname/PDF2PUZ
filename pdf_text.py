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
	indices = [None]
	num=1
	results = {}
	while indices:
		indices = [i.start() for i in re.finditer(str(num), raw)]
		results[num]=indices
		num += 1
	# any legit clue number should be listed in Across/Down as well as the grid
	# but I can't assume that will be true for OCR too
	#results = {k:v for k,v in results.items() if len(v) >= 2}
	print(results.keys())



if __name__ == '__main__':
	extract_clues(read('LAT'))