
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


def measure_chronologically_collated_tweets(topic="T1"):

	input_filename = "../data/corpora/twitter_topics/{}.csv".format(topic)
	results_filename = "../data/results/results_word_measures_twitter_topics_{}.csv".format(topic)

	N = 2000
	p_accept = 1

	simulated_post_words = []
	row_counter = 0

	df = pd.read_csv(input_filename)

	df['time'] = pd.to_datetime(df['time'])
	df_sorted = df.sort_values(by='time')
	df_sorted_unique = df_sorted.drop_duplicates("test")

	row_counter = 0
	for index,row in df_sorted_unique.iterrows():
		row_counter += 1
		if row_counter > 0:
			tweet_text = row["test"]
			words = clean_twitter_text(tweet_text)
			simulated_post_words += words

			if len(simulated_post_words) > 2100:
				clean_text = " ".join(simulated_post_words)

				analysis_name = "Twitter Topic {}".format(topic)

				metadata = [
					analysis_name, row_counter, "chrono_concat", "",
					"","", "word_measures", N
					]
				word_measures = measure_text_word_measures(clean_text, 2100)
				csv_row = metadata + word_measures
				print(csv_row)
				simulated_post_words = []
				append_to_csv(csv_row, results_filename)


def measure_all_topics():

	for j in range(11, 35):
		topic = "T{}".format(j+1)
		print("Working on topic ", j+1)
		measure_chronologically_collated_tweets(topic=topic)


def measure_all_topics_chronologically_collated():

	results_filename = "../data/results/results_word_measures_twitter_topics_combined.csv"
	# Create a dataframe 
	first_filename = "../data/corpora/twitter_topics/T1.csv"
	df = pd.read_csv(first_filename)

	print(len(df))

	for topic in range(2, 35):
		print(topic)
		input_filename = "../data/corpora/twitter_topics/T{}.csv".format(topic)
		next_df = pd.read_csv(input_filename)
		next_df = next_df.drop_duplicates("test")
		df = df.append(next_df)

		print(len(df))

	df['time'] = pd.to_datetime(df['time'])
	df_sorted = df.sort_values(by='time')
	df_sorted_unique = df_sorted.drop_duplicates("test")

	total_tweets = len(df_sorted_unique)
	print("Total tweets: ", total_tweets)

	N = 2000
	p_accept = 1

	simulated_post_words = []
	row_counter = 0

	for index,row in df_sorted_unique.iterrows():
		row_counter += 1
		if row_counter > 0:
			tweet_text = row["test"]
			words = clean_twitter_text(tweet_text)
			simulated_post_words += words

			if len(simulated_post_words) > 2100:
				clean_text = " ".join(simulated_post_words)

				analysis_name = "Twitter Topic {}".format(topic)

				metadata = [
					analysis_name, row_counter, "chrono_concat", "",
					"","", "word_measures", N
					]
				word_measures = measure_text_word_measures(clean_text, 2100)
				csv_row = metadata + word_measures
				print(csv_row)
				simulated_post_words = []
				append_to_csv(csv_row, results_filename)


if __name__=="__main__":
	measure_all_topics_chronologically_collated()