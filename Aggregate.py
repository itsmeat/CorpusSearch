ext = ".sgm"

import os
from bs4 import BeautifulSoup
import csv

cnt = 1
with open('docs.csv', 'a') as h:
	tocsv = csv.writer(h, delimiter = ',')
	for file in sorted(os.listdir('../reuters21578/')):
		if file.endswith(ext):
			text = ""
			with open(file, 'r', encoding = 'iso-8859-15') as handle:
				text = handle.read()
			soup = BeautifulSoup(text, 'lxml')
			text = soup.find_all("text")
			for i in text:
				if i.find('dateline') is not None:
					#print([cnt, i.find('title').string, i.find('dateline').string, i.get_text()])
					tocsv.writerow([cnt, i.find('title').string, i.find('dateline').string, i.get_text()])
					cnt = cnt + 1