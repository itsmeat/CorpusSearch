import pickle
import sys
import os
from math import log
from db_stats import load_dicts

def normalize(vector):

	length = 0
	vocab = list(vector.keys())
	count = len(vocab)
	mod_vector = {}

	for word in vocab:
		length += vector[word]*vector[word]

	for word in vocab:
		mod_vector[word] = ((vector[word]*vector[word])/length)**(0.5)#format((vector[word]*vector[word])/length, '.2f')

	return mod_vector

def vectorizer(loc_tf, idf, vocab = set()):
	
	loc_vector = {}
	loc_vocab = set(loc_tf.keys())
	if vocab:
		intersect = set.intersection(vocab, loc_vocab)
	else:
		intersect = loc_vocab
	
	for word in intersect:
	
		tf = 1 + (float)(log(loc_tf[word],10))
		loc_vector[word] = tf*idf[word]
	
	loc_vector = normalize(loc_vector)
	return loc_vector	
		
def load_vector(v_path):
	
	if os.path.exists(os.path.join(os.getcwd(), v_path)):
		with open(v_path, 'rb') as handle:
			dictionary = pickle.load(handle)

		doc_vector = dictionary['doc_vector']
		return doc_vector
	else:
		return []


def save_vector(v_path, doc_vector):

	dictionary = {}
	dictionary['doc_vector'] = doc_vector
	with open(v_path, 'wb') as handle:
		pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

def main():
	
	d_path = 'dict.pickle'
	v_path = 'vector.pickle'
	
	posting, vocab, doc_tf, idf = load_dicts(d_path)
	doc_vector = load_vector(v_path)
	
	no_of_vectors = len(doc_vector)
	no_of_docs = len(doc_tf)
	print ('No. of documents, no. of vectors: ', no_of_docs, no_of_vectors) 
	count = no_of_docs - no_of_vectors

	if count>0:

		#calculate idf of each word in vocab as it is constant for the whole corpus
		#idf = calculate_idf(posting, vocab, no_of_docs)		
		
		for i in range(0, count):
			
			print('Processing', i, 'document')
			loc_vector = vectorizer(doc_tf[i], idf)
			doc_vector.append(loc_vector)

	print('Processed new vectors:', count)
	if count:
		save_vector(v_path, doc_vector)

if __name__ == '__main__':
	main()