
import nltk.corpus.reader.bnc as cor
import os
import re
import numpy as np

from bs4 import BeautifulSoup

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utilities.general_utilities import append_to_csv

# Expects BNC data downloaded from https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2554#
# BNC data should be extracted and saved in "../data/corpora/bnc/raw/download"
# The "download" folder in the BNC should go there
# Also uses a BNC Corpus reader from the nltk module


def bnc_clean_text(text):

	# Remove commas and extra whitespace
 	text = remove_apostrophes_and_whitespace(text)
 	return text

def remove_apostrophes_and_whitespace(text):

	text = re.sub(r"\s{1,}", " ", text)
	text = re.sub(r"\s\'|\'", "", text)
	return text

def clean_bnc():

	in_file_directory = "../data/corpora/bnc/raw/download/Texts"
	out_file_directory = "../data/corpora/bnc/clean_text/"

	file_paths = []
	for dirname, dirnames, filenames in os.walk(in_file_directory):

		# get all file paths
		for filename in filenames:
			file_path = os.path.join(dirname, filename)
			file_paths.append(file_path)

	files_count = len(file_paths)
	
	row_counter = 0
	for file_path in file_paths:
		row_counter += 1
		if row_counter > 0:
			print("Working {} of {} - {} ".format(row_counter, files_count, file_path))
			try:
				file_root = "../"
				# Bit hacky - need a file root and this is an easy way to make that work	
				file_path = file_path.replace("../","")

				a=cor.BNCCorpusReader(root=file_root,fileids=file_path)
				raw_content = " ".join(a.words())
				content = bnc_clean_text(raw_content)

				id_code = file_path.split("/")[-1].replace(".xml", "")
				out_file_path = out_file_directory + id_code + ".txt"

				out_f = open(out_file_path, "w")
				out_f.write(content)
				out_f.close()
			except Exception as e:
				print(str(e))
				print("ERROR")
				raise
	

def extract_bnc_metadata():

	# Extarct bnc metadata

	# Title, Author, Year, Category
	in_file_directory = "../data/corpora/bnc/raw/download/Texts"
	out_file_path = "../data/results/bnc_metadata.csv"

	file_paths = []
	for dirname, dirnames, filenames in os.walk(in_file_directory):

		# get all file paths
		for filename in filenames:
			if filename[0] != ".":
				file_path = os.path.join(dirname, filename)
				file_paths.append(file_path)

	total_count = len(file_paths)

	counter = 0
	for file_path in file_paths:
		counter += 1
		print("Working on {} of {}".format(counter, total_count))

		id_code = file_path.split("/")[-1].replace(".xml", "")

		print("Working . . . ",  file_path)

		soup = BeautifulSoup(open(file_path, 'r'))

		# Year
		date_tag = soup.find('date')
		creation_tag = soup.find('creation')

		year = None
		if date_tag:
			year = date_tag.get_text()
		# Creation tag takes precedence over data tag
		if creation_tag:
			try:
				year = creation_tag["date"]
			except:
				pass

		# Author


		# Title
		title = None
		try:
			title = soup.find('title').get_text().strip()
		except:
			pass
	
		# Category
		category = None
		# Written text should have a wtext tag, spoken text should have a stext tag
		wtext_tag = soup.find('wtext')
		stext_tag = soup.find('stext')
		if wtext_tag:
			try:
				category = wtext_tag["type"]
			except:
				pass
		elif stext_tag:
			try:
				category = stext_tag["type"]
			except:
				pass

		csv_row = ["BNC", id_code, category, year, None, title]
		append_to_csv(csv_row, out_file_path)
		

if __name__=="__main__":
	extract_bnc_metadata()