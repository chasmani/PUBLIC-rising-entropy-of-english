
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))


import nltk
import os
import re

from utilities.gutenberg.src.cleanup import strip_headers

# Run this if you get an nltk LookUp error
# nltk.download('punkt')


def coha_clean_text(text):

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

def clean_all_coha():

	in_file_directory = "../data/corpora/coha/raw/"
	out_file_directory = "../data/corpora/coha/clean_text/"

	# Get text sample files
	files = os.listdir(in_file_directory)
	text_sample_files = [f for f in files if ".txt" in f]	
	
	total_file_count = len(text_sample_files)
	counter = 0

	for text_sample_file in text_sample_files:
		counter += 1
		print("Cleaning file {} of {}".format(counter, total_file_count))
		in_file_path = in_file_directory + text_sample_file
		out_file_path = out_file_directory + text_sample_file

		with open(in_file_path, 'r', errors="ignore") as f:
			content = f.read()
			content = coha_clean_text(content)
			
			out_f = open(out_file_path, "w")
			out_f.write(content)
			out_f.close()


if __name__=="__main__":
	clean_all_coha()
 	