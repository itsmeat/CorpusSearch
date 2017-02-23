from db_stats import load_dicts
from spell_check import P
import fnmatch

wild_card=raw_input('Enter your Wild card query')



posting, vocab, doc_tf, idf =load_dicts("dict.pickle");

filtered_list=fnmatch.filter(vocab,wild_card);

max = 0
max_w = ""
for word in filtered_list:
	prob=P(word)
	if prob > max : 
		max =prob
		max_w = word
print max_w
#num = 5
# ret_ls = []
# for c, key in enumerate(sorted(dict.keys(), reverse = True)):
# 	if c < num:
# 		ret_ls.append(dict[key])
# 	else:
# 		break
