
import csv
import random
import re
import nltk

import pandas as pd

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
	# Quite greedy - don't care too much about false positives
	# Any word with a fullstop within it, and at least one character either side
	text = re.sub(r"\@\S+", "", text)
	text = re.sub(r"\#\S+", "", text)
	return text


def clean_twitter_text(text):

	# Remove commas and extra whitespace
	text = remove_apostrophes_and_whitespace(text)

	text = remove_urls(text)
	
	text = remove_hashtags_and_usernames(text)

	tokens = nltk.tokenize.word_tokenize(text)

	words = [word.lower() for word in tokens if word.isalpha()]

	return words


def measure_chronologically_collated_tweets():

	input_filename = "../data/corpora/twitter_kaggle_sentiment140/raw/training.1600000.processed.noemoticon.csv"
	results_filename = "../data/results/results_word_measures_twitter.csv"

	N = 2000
	p_accept = 1

	simulated_post_words = []
	row_counter = 0
	with open(input_filename, 'r', encoding="ISO-8859-1") as read_obj:
		csv_reader = csv.reader(read_obj)
		for row in csv_reader:
			row_counter += 1

			# row variable is a list that represents a row in csv
			if random.random() < p_accept:
				post_content = row[5]
				words = clean_twitter_text(post_content)
			
				simulated_post_words += words

				if len(simulated_post_words) > 2100:
					clean_text = " ".join(simulated_post_words)

					metadata = [
					"Twitter", row_counter, "chrono_concat", 2009,
					"","", "word_measures", N
					]
					word_measures = measure_text_word_measures(clean_text, 2100)
					csv_row = metadata + word_measures
					simulated_post_words = []
					append_to_csv(csv_row, results_filename)


if __name__=="__main__":
	measure_chronologically_collated_tweets()