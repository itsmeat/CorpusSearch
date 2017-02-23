import nltk
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import csv

data = '/media/art/LocalDisk/Code/VENVS/scrap/reuters21578/docs.csv'

def tokenizer(sentence):
	return nltk.word_tokenize(sentence)

def lemmatizer(ls_words):
	pos_words = nltk.pos_tag(ls_words)
	wnl = WordNetLemmatizer()
	lem_words = [wnl.lemmatize(i,j[0].lower()).lower() if j[0].lower() in ['a','n','v'] else wnl.lemmatize(i) for i,j in pos_words]
	return lem_words

def main():

	with open(data, 'r') as handle:
		with open('./docs2.csv', 'w') as handl:
			reader = csv.reader(handle)
			writer = csv.writer(handl, delimiter = ',')
			for r in reader:
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

if __name__ == '__main__':
	main()
