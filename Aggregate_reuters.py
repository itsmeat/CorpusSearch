ext = ".sgm"

import os
from bs4 import BeautifulSoup
import csv

out_path = 'docs.csv'
reuters_path = '../reuters21578/'
cnt = 1

if not os.path.exists(out_path):
	with open(out_path, 'a') as h:
		tocsv = csv.writer(h, delimiter = ',')
		for file in sorted(os.listdir(reuters_path)):
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
else:
	print('file already exits')
