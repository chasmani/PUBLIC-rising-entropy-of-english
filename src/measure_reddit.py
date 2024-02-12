
from bs4 import BeautifulSoup
import csv
import random
import json
import re
import langdetect
import nltk

import pandas as pd
pd.set_option('display.max_columns', None)

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utilities.text_measures import measure_text_word_measures
from utilities.general_utilities import append_to_csv


def remove_apostrophes_and_whitespace(text):

	text = re.sub(r"\s{1,}", " ", text)
	text = re.sub(r"\s\'|\'", "", text)
	return text

def remove_urls(text):
	# Quite greedy - don't care too much about false positives
	# Any word with a fullstop within it, and at least one character either side
	text = re.sub(r"\S+\.\S+", "", text)
	return text


def remove_hashtags_and_usernames(text):
	
	text = re.sub(r"\@\S+", "", text)
	text = re.sub(r"\#\S+", "", text)
	return text


def clean_reddit_text(text):

	# Remove commas and extra whitespace
	text = remove_apostrophes_and_whitespace(text)

	text = remove_urls(text)
	
	text = remove_hashtags_and_usernames(text)

	tokens = nltk.tokenize.word_tokenize(text)

	words = [word.lower() for word in tokens if word.isalpha()]

	return words


def measure_reddit():

	text_samples = extract_all_posts()
	print(len(text_samples))

	results_filename = 	"../data/results/results_word_measures_reddit.csv"

	sample_id = 0

	h1s = []
	ttrs = []

	for text_sample in text_samples:
		
		sample_id += 1
		metadata = ["Reddit", sample_id, "homepage", 2023, None, None, "word_measures", 2000]

		print(len(text_sample))
		print("Unique types:", len(set(text_sample)))

		text_sample_string = " ".join(text_sample)

		#print(text_sample_string)

		word_measures = measure_text_word_measures(text_sample_string, 2100)
		print(word_measures)

		csv_list = metadata + word_measures

		append_to_csv(csv_list, results_filename)

		h1s.append(word_measures[6])
		ttrs.append(word_measures[2])
		
	print(sample_id)
	import numpy as np
	print(np.mean(h1s))
	print(np.mean(ttrs))

def extract_all_posts():

	all_post_strings = []
	unique_post_ids = set()

	post_lengths = []

	import os
	reddit_data_folder = "../data/corpora/reddit/"
	only_files = [os.path.join(reddit_data_folder, f) for f in os.listdir(reddit_data_folder) if os.path.isfile(os.path.join(reddit_data_folder, f))]
	only_json_files = [f for f in only_files if "reddit_json" in f]

	for input_filename in only_json_files:

		json_text = open(input_filename, "r").read()
		json_data = json.loads(json_text)

		posts = json_data["data"]["children"]
		for post in posts:
			unique_post_id = post["data"]["id"]
			if unique_post_id not in unique_post_ids:
				unique_post_ids.add(unique_post_id)
				post_string = post["data"]["title"]
				post_text = post["data"]["selftext"]
				if post_text != "":
					post_string += " " + post_text

				try:
					# Exception if post text is all emojis etc
					if langdetect.detect(post_string) == "en":
						all_post_strings.append(post_string)
				except:
					pass

	combined_text_samples = []

	this_combined_post_words = []

	for text_sample in all_post_strings:

		clean_words = clean_reddit_text(text_sample)
		
		post_lengths.append(len(clean_words))
		this_combined_post_words += clean_words

		if len(this_combined_post_words) > 2100:
			combined_text_samples.append(this_combined_post_words)
			this_combined_post_words = []

	print("Total unique reddit posts:", len(all_post_strings))

	print("Total number of collated samples:", len(combined_text_samples))
	return combined_text_samples
	

if __name__=="__main__":
	extract_all_posts()