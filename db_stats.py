import csv
import nltk
import numpy as np
import pickle
import os
import sys
from math import log


def give_loc_tf(text):

	ls_text = [x.lower() for x in text.split()]
	freq = nltk.FreqDist(ls_text)

	ls = freq.most_common(len(freq))
	loc_tf = {}
	for x in ls:
		loc_tf[x[0]] = x[1]

	return loc_tf

def calculate_idf(posting, vocab, no_of_docs):

	idf = {}
	
	for word in vocab:
		idf[word] = (float)(log(no_of_docs/len(posting[word]), 10))

	return idf

def vocab_update(loc_vocab, vocab):

	vocab.update(loc_vocab)

def posting_update(loc_vocab, doc_id, posting):

	for x in loc_vocab:
		if x not in posting.keys():
			posting[x] = set()
		posting[x].update([doc_id])

def load_dicts(path):

	if os.path.exists(os.path.join(os.getcwd(), path)):
		with open(path, 'rb') as handle:
			dictionary = pickle.load(handle)

		posting = dictionary['posting']
		vocab = set(dictionary['vocab'])
		doc_tf = dictionary['doc_tf']
		idf = dictionary['idf'] 

		return posting, vocab, doc_tf, idf
	else:
		return {}, set(), [], {}

def save_dicts(path, posting, vocab, doc_tf, idf):
	
	dictionary = {}
	dictionary['posting'] = posting
	dictionary['vocab'] = list(vocab)
	dictionary['doc_tf'] = doc_tf
	dictionary['idf'] = idf		

	with open(path, 'wb') as handle:
		pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

def read_my_lines(csv_reader, no_of_docs):
	
	for line_number, row in enumerate(csv_reader, 1):
		if line_number > no_of_docs:
			#print('should not happen')
			yield line_number, row
			
def main():
	
	data = './docs2.csv'
	count = 0
	path = 'dict.pickle'
	
	posting, vocab, doc_tf, idf = load_dicts(path)
	no_of_docs = len(doc_tf)		
	print(no_of_docs)

	reader = csv.reader(open(data, 'r'))
	for line_number, row in read_my_lines(reader, no_of_docs):
		text = row[5]
		count+= 1
		print('Processing', count)
		
		loc_tf = give_loc_tf(text)
		loc_vocab = list(loc_tf.keys())
		doc_tf.append(loc_tf)
		
		vocab_update(loc_vocab, vocab)
		posting_update(loc_vocab, line_number, posting)
	

	print('No. of new documents, total docs: ', count, len(doc_tf))
	print('Size of vocabulary: ', len(vocab))

	#calculate idf, since all documents scanned
	if count:
		idf = calculate_idf(posting, vocab, no_of_docs+count)
		save_dicts(path, posting, vocab, doc_tf, idf)

if __name__ == '__main__':
	main()