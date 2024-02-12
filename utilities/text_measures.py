

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import re
from collections import Counter
import numpy as np
import csv
import os
import nltk

from utilities.general_utilities import append_to_csv
from utilities.zipfanalysis_clauset import clauset_estimator, clauset_estimator_frequency_counts

#5. Entropies
def get_entropies(words):
	
	H_0 = np.log2(len(words))

	H_1 = 0
	counter_1 = Counter(words)
	total_words = len(words)
	for k,v in counter_1.most_common():
		p = v/total_words
		H_1 += -p*np.log2(p)

	H_2 = 0
	counter_2 = Counter()
	for i in range(total_words-1):
		gram_2 = words[i] + " " + words[i+1]
		counter_2[gram_2] += 1
	total_2_grams = total_words - 1
	
	for k,v in counter_2.most_common():
		p = v/total_words
		H_2 += -p*np.log2(p)			

	return [H_0, H_1, H_2]

def measure_zipf_exponents(words):

	word_counts = Counter(words)
	ns = [v for k,v in word_counts.most_common()]

	gamma_clauset = clauset_estimator_frequency_counts(ns)
	alpha_clauset = clauset_estimator(ns)

	return [gamma_clauset, alpha_clauset]


def measure_text_word_measures(text, word_count):

	tokens = nltk.tokenize.word_tokenize(text)

	words = [word.lower() for word in tokens if word.isalpha()]
	
	if len(words)>word_count:
		words = words[:word_count]
	else:
		return None

	# Get middle sample of words, ignoring a buffer of total size 100 words at start and end
	middle = len(words) // 2
	actual_word_count = word_count - 100
	start = middle - actual_word_count // 2
	end = start + actual_word_count
	words = words[start:end]

	# Average word length
	word_lengths = [len(word) for word in words]
	avg_word_length = np.mean(word_lengths)

	# Type token ratio
	ttr = len(set(words))/len(words)

	# zipf exponent
	zipfs = measure_zipf_exponents(words)

	# Word entropies
	entropies = get_entropies(words)

	measurements = [word_count, avg_word_length, ttr] + zipfs + entropies

	return measurements


def test_file():

	filename = "../data/corpora/coca_free/clean_text/acad_coca_2.txt"
	
	with open (filename, 'r', errors="ignore") as f:
		text = f.read()
		print(measure_text_word_measures(text, 2100))

def test_dummy():

	num_str = [str(i) for i in range(2100)]
	dummy_text = " ".join(num_str)
	print(measure_text_word_measures(dummy_text, 2100))


if __name__=="__main__":
	
	test_dummy()