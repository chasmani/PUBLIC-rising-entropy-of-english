

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pandas as pd
import csv


def count_all_coha():

	in_file_directory = "../data/corpora/coha/raw/"

	# Get text sample files
	files = os.listdir(in_file_directory)
	text_sample_files = [f for f in files if ".txt" in f]	
	
	total_file_count = len(text_sample_files)
	counter = 0

	fic_counter = 0
	nf_counter = 0
	mag_counter = 0
	news_counter = 0

	for text_sample_file in text_sample_files:
		
		if "fic" in text_sample_file:
			fic_counter += 1
		elif "nf" in text_sample_file:
			nf_counter += 1
		elif "mag" in text_sample_file:
			mag_counter += 1
		elif "news" in text_sample_file:
			news_counter += 1
		else:
			print("Not in a known category ", text_sample_file)


	print("Fic: ", fic_counter)
	print("NF: ", nf_counter)
	print("Mags: ", mag_counter)
	print("News: ", news_counter)
	print("Total: ", fic_counter + nf_counter + mag_counter + news_counter)


def count_coca_free():

	in_file_directory = "../data/corpora/coca_free/raw/"


	total_count = 0
	for filename in ["text_fic.txt", "text_acad.txt", "text_mag.txt", "text_news.txt"]:

		this_dir = in_file_directory + filename

		num_lines = 0

		with open(this_dir, 'r') as f:
		    for line in f:
		        num_lines += 1

		total_count += num_lines

		print(filename, num_lines)

	print("Total ", total_count)


def count_bnc():

	counter = 0

	fic_counter = 0
	nf_counter = 0
	mag_counter = 0
	news_counter = 0

	metadata_filename = "../data/results/bnc_metadata.csv"
	with open(metadata_filename, 'r', encoding="utf-8") as read_obj:
		csv_reader = csv.reader(read_obj, delimiter=";")
		for row in csv_reader:
			print(row[2])


			counter += 1


			if row[2] == "FICTION":
				fic_counter += 1
			elif row[2] == "ACPROSE":
				nf_counter += 1
			elif row[2] == "NEWS":
				news_counter += 1



	print("Fic: ", fic_counter)
	print("NF: ", nf_counter)
	print("News: ", news_counter)
	print("Total: ", counter)
	


metadata_headers = [
		"source",
		"sample_id", 
		"category", 
		"year", 
		"author", 
		"title", 
		"measure_type",
		"length"]

word_measures_headers = [
	"word_count", 
	"avg_word_length", 
	"ttr",
	"zipf_cdf",
	"zipf_clauset", 
	"H_0",
	"H_1",
	"H_2"]
	

def summarise_measures_coha():
	headers = metadata_headers + word_measures_headers

	input_filename = "../data/results/results_word_measures_coha.csv"
	df_coha = pd.read_csv(input_filename, delimiter=";", names=headers)
	# Recent COHA

	df_coha = df_coha[(df_coha['length'] == 2000)]
	print(len(df_coha))

	for category in ["mag", "news", "", "fic", "nf"]:
		df_category = df_coha[(df_coha['category'] == category)]
		print(category, len(df_category))


def summarise_measures_coca():
	headers = metadata_headers + word_measures_headers

	input_filename = "../data/results/results_word_measures_coca.csv"
	df_coca = pd.read_csv(input_filename, delimiter=";", names=headers)
	# Recent COHA

	df_coca = df_coca[(df_coca['length'] == 2000)]
	print(len(df_coca))

	for category in ["mag", "news", "acad", "fic"]:
		df_category = df_coca[(df_coca['category'] == category)]
		print(category, len(df_category))

def summarise_measures_bnc():
	headers = metadata_headers + word_measures_headers

	input_filename = "../data/results/results_word_measures_bnc.csv"
	df_coca = pd.read_csv(input_filename, delimiter=";", names=headers)
	# Recent COHA

	df_coca = df_coca[(df_coca['length'] == 2000)]
	print(len(df_coca))

	counter = 0

	for category in ["FICTION", "ACPROSE", "NEWS"]:
		df_category = df_coca[(df_coca['category'] == category)]
		print(category, len(df_category))
		counter += len(df_category)
	print(counter)




if __name__=="__main__":
	summarise_measures_bnc()