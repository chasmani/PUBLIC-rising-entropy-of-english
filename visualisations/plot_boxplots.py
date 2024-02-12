


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from design_scheme import COLOR_NF, COLOR_FIC, COLOR_NEWS, COLOR_MAG, COLOR_SOCIAL, LINEWIDTH


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
	

def coha_boxplots(measure="H_1"):


	measure_type = "word_measures"
	headers = metadata_headers + word_measures_headers

	input_filename = "../data/results/results_{}_coha.csv".format(measure_type)
	df_coha = pd.read_csv(input_filename, delimiter=";", names=headers)
	# Recent COHA
	df_coha = df_coha[(df_coha['year'] > 1999)]
	# Rmeove an outlier in COHA
	df_coha = df_coha[(df_coha['H_1'] > 6)]

	
	
	coha_categories = ["mag", "news", "", "fic", "nf"]
	coha_verbose = ["Mag", "News", "", "Fiction", "Non-Fic"]

	source_cats_order = [
		
		"Twitter ",
		"",
		"COHA news",
		"COHA mag",
		"COCA news",
		"COCA mag",
		"BNC NEWS",
		"",
		"COHA nf",
		"COHA fic", 
		"COCA acad", 
		"COCA fic",
		"BNC ACPROSE",
		"BNC FICTION"
	]

	N = 2000

	df_coha = df_coha[(df_coha['length'] == float(N))]	
	

	sns.boxplot(data=df_coha, y=measure, x="category", orient="v", order=coha_categories, linewidth=2)


	plt.xticks(range(len(coha_verbose)), coha_verbose, rotation=45, ha='right')
	ax = plt.gca()
	ax.yaxis.grid(True)



def combined_snapshots(measure="H_2", measure_name="Bigram Entropy"):


	headers = metadata_headers + word_measures_headers
	
	input_filename = "../data/results/results_word_measures_coca.csv"
	df_coca = pd.read_csv(input_filename, delimiter=";", names=headers)

	input_filename = "../data/results/results_word_measures_coha.csv"
	df_coha = pd.read_csv(input_filename, delimiter=";", names=headers)

	input_filename = "../data/results/results_word_measures_bnc.csv"
	df_bnc = pd.read_csv(input_filename, delimiter=";", names=headers)

	input_filename = "../data/results/results_word_measures_twitter.csv"
	df_twitter = pd.read_csv(input_filename, delimiter=";", names=headers)

	input_filename = "../data/results/results_word_measures_twitter_topics_combined.csv"
	df_twitter_topics = pd.read_csv(input_filename, delimiter=";", names=headers)

	input_filename = "../data/results/results_word_measures_reddit.csv"
	df_reddit = pd.read_csv(input_filename, delimiter=";", names=headers)

	pd.set_option('display.max_columns', None)

	# Recent COHA
	df_coha = df_coha[(df_coha['year'] > 1999)]
	# Rmeove an outlier in COHA
	#df_coha = df_coha[(df_coha['H_1'] > 6)]

	outlier_sd = 5
	outlier_count = 0
	# Remove outliers 
	coha_len = len(df_coha)
	coha_sd = df_coha[measure].std()
	coha_mean = df_coha[measure].mean()
	df_coha = df_coha[(df_coha[measure] < coha_mean + outlier_sd*coha_sd)]
	df_coha = df_coha[(df_coha[measure] > coha_mean - outlier_sd*coha_sd)]
	outlier_count += coha_len - len(df_coha)

	coca_len = len(df_coca)
	coca_sd = df_coca[measure].std()
	coca_mean = df_coca[measure].mean()
	df_coca = df_coca[(df_coca[measure] < coca_mean + outlier_sd*coca_sd)]
	df_coca = df_coca[(df_coca[measure] > coca_mean - outlier_sd*coca_sd)]
	outlier_count += coca_len - len(df_coca)

	bnc_len = len(df_bnc)
	bnc_sd = df_bnc[measure].std()
	bnc_mean = df_bnc[measure].mean()
	df_bnc = df_bnc[(df_bnc[measure] < bnc_mean + outlier_sd*bnc_sd)]
	df_bnc = df_bnc[(df_bnc[measure] > bnc_mean - outlier_sd*bnc_sd)]
	outlier_count += bnc_len - len(df_bnc)

	twitter_len = len(df_twitter)
	twitter_sd = df_twitter[measure].std()
	twitter_mean = df_twitter[measure].mean()
	df_twitter = df_twitter[(df_twitter[measure] < twitter_mean + outlier_sd*twitter_sd)]
	df_twitter = df_twitter[(df_twitter[measure] > twitter_mean - outlier_sd*twitter_sd)]
	outlier_count += twitter_len - len(df_twitter)

	twitter_topics_len = len(df_twitter_topics)
	twitter_topics_sd = df_twitter_topics[measure].std()
	twitter_topics_mean = df_twitter_topics[measure].mean()
	df_twitter_topics = df_twitter_topics[(df_twitter_topics[measure] < twitter_topics_mean + outlier_sd*twitter_topics_sd)]
	df_twitter_topics = df_twitter_topics[(df_twitter_topics[measure] > twitter_topics_mean - outlier_sd*twitter_topics_sd)]
	outlier_count += twitter_topics_len - len(df_twitter_topics)
	print(twitter_topics_len - len(df_twitter_topics))

	reddit_len = len(df_reddit)
	reddit_sd = df_reddit[measure].std()
	reddit_mean = df_reddit[measure].mean()
	df_reddit = df_reddit[(df_reddit[measure] < reddit_mean + outlier_sd*reddit_sd)]
	df_reddit = df_reddit[(df_reddit[measure] > reddit_mean - outlier_sd*reddit_sd)]
	outlier_count += reddit_len - len(df_reddit)

	print("Removed {} outliers".format(outlier_count))


	# Combine all into one df
	df = pd.concat([df_coca, df_coha, df_bnc, df_twitter, df_twitter_topics, df_reddit])
	print("Total observations are ", len(df))

	df.replace(to_replace="Twitter Kaggle Sentiment", value="Twitter", inplace=True)
	df.replace(to_replace="Twitter Topic 34", value="Twitter 2020", inplace=True)
	df.replace(to_replace="chrono_concat", value="", inplace=True)
	df.replace(to_replace="chrono_concat_truncated", value="", inplace=True)

	df.replace(to_replace="homepage", value="", inplace=True)

	df.replace(to_replace="collated-255", value="", inplace=True)

	df["source category"] = df["source"] + " " + df["category"]

	print(df["source category"].unique())

	all_cats_list = [""]*17

	social_cats = all_cats_list.copy()
	social_cats[1] = "Reddit "
	social_cats[2] = "Twitter 2020 "
	social_cats[3] = "Twitter "

	short_form_cats = all_cats_list.copy()
	short_form_cats[5] = "COHA news"
	short_form_cats[6] = "COHA mag"
	short_form_cats[7] = "COCA news"
	short_form_cats[8] = "COCA mag"
	short_form_cats[9] = "BNC NEWS"

	long_form_cats = all_cats_list.copy()
	long_form_cats[11] = "COHA nf"
	long_form_cats[12] = "COHA fic"
	long_form_cats[13] = "COCA acad"
	long_form_cats[14] = "COCA fic"
	long_form_cats[15] = "BNC ACPROSE"
	long_form_cats[16] = "BNC FICTION"

	category_ticks = ["", "Reddit 2023", "Twitter 2020", "Twitter 2009", "", "COHA News", "COHA Magazines", 
		"COCA News", "COCA Magazines", "BNC News", "", "COHA Non-Fiction",
		"COHA Fiction", "COCA Non-Fiction", "COCA Fiction", "BNC Non-Fiction", 
		"BNC Fiction"]


	N = 2000

	df = df[(df['length'] == float(N))]	
	
	df['H_1_neg'] = 0 - df['H_1']

	df = df.append([-999,-999,-999,-999,'setosa'])
	df['huecol'] = 0.0
	df['huecol'].iloc[-1]= 999

	ax = plt.gca()



	# Socials
	sns.violinplot(data=df, x=measure, y="source category", saturation=0.4, width=1.5, cut=0, inner="quartile", split=True, hue="huecol",  order=social_cats, linewidth=2, palette=[COLOR_SOCIAL])

	# Short form 
	sns.violinplot(data=df, x=measure, y="source category", saturation=0.4, width=1.5, cut=0, inner="quartile", split=True, hue="huecol",  order=short_form_cats, linewidth=2, palette=[COLOR_MAG])

	# Long form 
	sns.violinplot(data=df, x=measure, y="source category", saturation=0.4, width=1.5, cut=0, inner="quartile", split=True, hue="huecol",  order=long_form_cats, linewidth=2, palette=[COLOR_NF])


	plt.ylabel("")
	plt.xlabel(measure_name)

	plt.yticks(range(len(category_ticks)), category_ticks)

	plt.grid(axis="x")


	ax = plt.gca()
	ax.legend().set_visible(False)

	if measure == "zipf_clauset":
		ax.invert_xaxis()

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['left'].set_visible(False)

	ax.yaxis.set_label_position("right")
	ax.yaxis.tick_right()
	ax.yaxis.set_ticks_position('none')
	plt.yticks(va="bottom")

	plt.savefig("images/word_measure_distributions_{}.tiff".format(measure), format="tiff", dpi=300)
	plt.savefig("images/word_measure_distributions_{}.png".format(measure), format="png", dpi=300)


if __name__=="__main__":
	fig_width, fig_height = plt.gcf().get_size_inches()

	fig = plt.figure(figsize=(fig_width, fig_height), constrained_layout=True)
	
	combined_snapshots(measure="H_1", measure_name="Word Entropy")

	plt.show()