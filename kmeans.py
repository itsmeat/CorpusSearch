from vector import load_vector
import numpy as np
from db_stats import load_dicts
import matplotlib.pyplot as plt 
from sklearn.manifold import TSNE
from gensim import matutils
import pickle

def plt_tsne(mat, no_of_vectors):

	tsne = TSNE(n_components=2, random_state=0)
	np.set_printoptions(suppress=True)

	Y = tsne.fit_transform(mat)

	plt.scatter(Y[:, 0], Y[:, 1])
	for i in range(no_of_vectors):
	    plt.annotate(vocabulary[i], xy=(Y[i, 0], Y[i, 1]), xytext=(0, 0), textcoords='offset points')
	plt.show()

def main():

	v_path = 'vector.pickle'
	d_path = 'dict.pickle'

	doc_vector = load_vector(v_path)
	posting, vocab, doc_tf, idf = load_dicts(d_path)
	arr = []
	cnt = 0
	for loc_vector in doc_vector:
	
		print(cnt)
		loc_list = []
		for c, word in enumerate(vocab, 1):
			if word in loc_vector:
				loc_list.append((c, loc_vector[word]))
		arr.append(loc_list)
		cnt += 1
	dictionary = {}
	dictionary['vector_id'] = arr
	with open('vector_id.pickle', 'wb') as h:
		pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
	corpus_tfidf = matutils.corpus2csc(arr).transpose()
	print(len(corpus_tfidf))

if __name__ == '__main__':
	main()