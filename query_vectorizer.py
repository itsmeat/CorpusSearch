from tok_lem import tokenizer, lemmatizer
from db_stats import give_loc_tf, load_dicts
from vector import vectorizer, load_vector
import csv
from spell_check import correction
import enchant
from spell_check import P
import fnmatch
import os


d_path = 'dict.pickle'
v_path = 'vector.pickle'
data = './docs2.csv'
no_to_fetch = 10

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

def func(word, vocab):
	filtered_list=fnmatch.filter(vocab,word);

	max = 0
	max_w = ""
	for word in filtered_list:
		prob=P(word)
		if prob > max : 
			max =prob
			max_w = word
	return max_w


def handle_wildcard(list_of_words, vocab):
	ret_ls = []
	for word in list_of_words:
		f = 0
		for x in range(0, len(word)):
			if word[x] == '*':
				f = 1
				break
		if f:
			ret_ls.append(func(word, vocab))
		else:
			ret_ls.append(word)
	return ret_ls

def start(posting,vocab,doc_tf,idf,doc_vector):

	q_raw = input("Enter your query: ")
	option_num = input("Enter an option number (1-3) :")
	
	q_tok = tokenizer(q_raw)
	#check for wildcard queries
	q_tok2 = handle_wildcard(q_tok, vocab)
	#1
	


	#2 context
	#d = enchant.Dict("en_US")
	#q_spell2 = [d.suggest(word)[0] for word in q_spell]

	q_proc = lemmatizer(q_tok2)	
	


	q_spell = [correction(word) for word in q_proc]
	q_spell = " ".join(q_spell)
	

	q_vector = vectorizer(give_loc_tf(q_spell), idf, vocab)
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
			#print(score[key],': ' ,key)
			count += 1
		else:
			break

	reader = csv.reader(open(data, 'r'))

	to_print = {}
	for line_number, row in read_my_lines(reader, lines_set):
		to_print[line_number] = row[3] 

	if option_num == '1':
		print(" ")
		print ("Tokenizer Ouput: ", q_tok2);
		
		print(" ")
		print ("Lemmatizer Output: ",q_proc);


	if option_num == '2':
		print(" ")
		print ("Spelling Correction: ", q_spell)


	if option_num == '3':
		print ("Documents returned: ")

		for i in lines_set:
			print ('\n')
			print ("**************Document Number-"+str(i)+"  *******************")
			print(to_print[i])
			print('\n') 



	test=input("Press 0 to exit from Search Engine, else press any other key to search again...");

	return test








def main():
	try:
   		input = raw_input
	except NameError:
   		pass	

	os.system('clear');
	print ('Loading Document Vectors......')

	posting, vocab, doc_tf, idf = load_dicts(d_path)
	doc_vector = load_vector(v_path)

	test=' ';

	while test!='0':
		if test!=' ':
			os.system('clear');
		else:
			print('\nDocument vectors Loaded.')

		print('\n\n');
		test=start(posting,vocab,doc_tf,idf,doc_vector);
	



		
if __name__ == '__main__':
	main()
