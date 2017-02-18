from tok_lem import tokenizer, lemmatizer
from db_stats import give_loc_tf, load_dicts
from vector import vectorizer, load_vector
import csv

def give_score(q_vector, loc_vector, q_vocab):

	loc_vocab = set(loc_vector.keys())

	intersect = set.intersection(q_vocab, loc_vocab)

	loc_score = 0
	for word in intersect:
		loc_score += q_vector[word]*loc_vector[word]#float(q_vector[word])*float(loc_vector[word])

	return loc_score#format(loc_score, '.2f')

def read_my_lines(csv_reader, lines_list):
	# make sure every line number shows up only once:
	lines_set = set(lines_list)
	for line_number, row in enumerate(csv_reader, 1):
		if line_number in lines_set:
			yield line_number, row
			lines_set.remove(line_number)
			# Stop when the set is empty
			if not lines_set:
				break

def main():
	
	d_path = 'dict.pickle'
	v_path = 'vector.pickle'
	data = './docs2.csv'
	no_to_fetch = 5

	q_raw = input('Enter your query:')
	q_proc = " ".join(lemmatizer(tokenizer(q_raw)))
	
	posting, vocab, doc_tf, idf = load_dicts(d_path)
	doc_vector = load_vector(v_path)
	
	q_vector = vectorizer(give_loc_tf(q_proc), idf, vocab)
	q_vocab = set(q_vector.keys())
		
	no_of_docs = len(doc_vector)
	score = {}
	#score2 = {}
	for i in range(0, no_of_docs):

		loc_score = give_score(q_vector, doc_vector[i], q_vocab)
		score[loc_score] = i+1 
		#score2[i+1] = loc_score

	#print(len(list(score.keys())), len(list(score2.keys())))
	
	count = 0
	lines_set = []
	for key in sorted(score.keys(), reverse = True):
		if count < no_to_fetch:
			lines_set.append(score[key])
			print(score[key],': ' ,key)
			count += 1
		else:
			break

	reader = csv.reader(open(data, 'r'))

	to_print = {}
	for line_number, row in read_my_lines(reader, lines_set):
		to_print[line_number] = row[3] 

	for i in lines_set:
		print(to_print[i])
		print('\n')
		
if __name__ == '__main__':
	main()