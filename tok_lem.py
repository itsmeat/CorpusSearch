import nltk
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import csv
import os
from nltk.corpus import stopwords
from db_stats import read_my_lines
from bs4 import BeautifulSoup
import regex

stops = set(stopwords.words('english'))
data = 'docs.csv'

single = ['a', 'i', 'o']
double_c = ['ll', 've', 'em', 're']
contractions = {"ain't": "am not", "can't": "cannot", "won't": "will not", "n't": " not",\
				"gonna": "going to", "gotta": "got to","he's": "he is", "she's": "she is", "it's": "it is",\
				"'d": " had", "'ll": " will", "'ve": " have", "'m": " am", "'re": " are", "'em": " them"}
contractions_list = ["ain't", "can't", "won't", "n't", "gonna", "gotta", "he's", "she's", "it's", "'d", "'ll", "'ve", "'m", "'re", "'em"]
#ambiguous : "gotta": "got to/got a", "ain't": "am/is/are/.. not", "'s": depends on preword


def helper_func(ele):
	ls = ele.group(0).split("'")
	if ls[0] == "":
		return ele.group(0)
	#print(ls[0]+contractions["'"+ls[1]])
	return ls[0]+contractions["'"+ls[1]]

def pprocess(raw_review, is_make_dict = 0, remove_stopwords = False):
	# remove html tags if any
	raw_review = BeautifulSoup(raw_review, 'lxml').get_text()
	
	# remove the urls
	review_text = regex.sub(r"http\S+", "", raw_review)
	
	# uniformise the quotation marks for the next operation of contraction expansion
	review_text = regex.sub('[\p{QuotationMark}]', '\'', review_text)
	
	#lower case
	review_text = review_text.lower()
	 
	# remove all the non-ascii characters--improve this to substitute contractions eg: n't -> not, he's-> he is
	# but beware of eg: man's life..
	for x in contractions_list:
		if(x in contractions_list[-6:len(contractions_list)]):
			review_text = regex.sub("\S+"+x, helper_func, review_text)
		else:
			review_text = regex.sub(x, contractions[x], review_text)
	#make words only 
	#review_text = remove_non_ascii(review_text)
	letters_only = regex.sub("[^a-zA-Z]", " ", review_text)
	#tokenize
	words = letters_only.split()
	ret = []
	#check for any non-meaningful one letter or two lettered words 
	for c, word in enumerate(words):
		if len(word) is 2 and word in double_c:
			continue
		if len(word) is 1 and word not in single:
			continue
		ret.append(word)
	#remove stopwords if specified
	if remove_stopwords:
		words = [w for w in words if not w in stopwords]
	#set for faster processing
	if is_make_dict:	
		return set(ret)
	else:
		return ret	

def tokenizer(sentence):
	#return nltk.word_tokenize(sentence)
	return pprocess(sentence)

def lemmatizer(ls_words):
	pos_words = nltk.pos_tag(ls_words)
	wnl = WordNetLemmatizer()
	lem_words = [wnl.lemmatize(i,j[0].lower()).lower() if j[0].lower() in ['a','n','v'] else wnl.lemmatize(i) for i,j in pos_words]
	return lem_words

def main():

	data_path = 'docs.csv'
	out_path = 'docs2.csv'

	if os.path.exists(out_path):
		with open(out_path,"r") as f:
			reader = csv.reader(f,delimiter = ",")
			data = list(reader)
			row_count = len(data)
	else:
		row_count = 0

	print("No. of already processed docs: ",row_count)

	count = 0
	with open(data_path, 'r') as handle:
		with open(out_path, 'a') as handl:
			reader = csv.reader(handle)
			writer = csv.writer(handl, delimiter = ',')
			for line_number, r in read_my_lines(reader, row_count):
				count += 1
				print ("processing ", count, " document.")
				text = r[3]
				lem_text = ""
				tok_text = ""
				sentences = nltk.sent_tokenize(text)
				for sentence in sentences:
					ls_words = tokenizer(sentence)
					
					lem_words = lemmatizer(ls_words)
					lem_text = lem_text + (" ".join(lem_words))
					tok_text = tok_text + (" ".join(ls_words))

				writer.writerow([r[0], r[1], r[2], r[3], tok_text, lem_text])
				

	print("New processed documents: ", count)

if __name__ == '__main__':
	main()
