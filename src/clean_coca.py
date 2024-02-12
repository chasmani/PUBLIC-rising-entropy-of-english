
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import nltk
import os
import re

from utilities.gutenberg.src.cleanup import strip_headers

def coca_clean_text(text):

	# Remove PG
 	text = remove_pg_blurb(text)
 	# Remove tags e.g. <P>
 	text = remove_tags(text)
 	
 	# Remove funky sentences
 	text = remove_funky_sentences(text)
 	# Remove commas and extra whitespace
 	text = remove_apostrophes_and_whitespace(text)
 	return text

def remove_apostrophes_and_whitespace(text):

	text = re.sub(r"\s{1,}", " ", text)
	text = re.sub(r"\s\'|\'", "", text)
	return text

def remove_pg_blurb(text):
	# Use the Gutenberg standard project's cleaner
 	return strip_headers(text)

def remove_funky_sentences(text):
	# remove sentences with "@"
 	sents = nltk.tokenize.sent_tokenize(text)
 	clean_sents = [sent for sent in sents if "@" not in sent]
 	return " ".join(clean_sents)

def remove_tags(text):
	text = re.sub(r"\<.*?\>", "", text)
	return text

def clean_all_coca():

	in_file_directory = "../data/corpora/coca_free/raw/"
	out_file_directory = "../data/corpora/coca_free/clean_text/"

	# Get text sample files
	files = os.listdir(in_file_directory)
	text_sample_files = [f for f in files if ".txt" in f]	
	
	# One sample per line
	for text_sample_file in text_sample_files:
		
		filein = open(in_file_directory + text_sample_file, 'r')
		lines = filein.readlines()

		line_count = 0

		category = text_sample_file.split("_")[1].replace(".txt", "")

		for line in lines:
			line_count += 1
			print(line_count)

			content = coca_clean_text(line)

			out_file_path = out_file_directory + "{}_coca_{}.txt".format(category, line_count)

			out_f = open(out_file_path, "w")
			out_f.write(content)
			out_f.close()


if __name__=="__main__":
	clean_all_coca()
 	