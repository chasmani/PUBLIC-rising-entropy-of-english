


import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms

from matplotlib import style


from plot_timeseries import get_timeseries_combined_plot_with_conf_intervals
from plot_prey_choice_diet_distributions import plot_prey_diet_choice_distribution
from plot_rising_entropy_model import entropy_rising_simulation

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10})



def big_fig(N=2000):


	fig_width, fig_height = plt.gcf().get_size_inches()

	fig = plt.figure(figsize=(fig_width*1.5, fig_height*1.5), constrained_layout=True)
	
	#fig = plt.figure(figsize=(fig_width*2, fig_height), constrained_layout=True)


	# nrows
	gs = fig.add_gridspec(nrows=2, ncols=3)

	# Top Left - Timeseries
	ax1 = plt.subplot(gs[:,:2])

	get_timeseries_combined_plot_with_conf_intervals(measure="H_1", N=N)
	plt.xlabel("Year")
	plt.ylabel("Word Entropy")

	ax1.spines['right'].set_visible(False)
	ax1.spines['top'].set_visible(False)
	ax1.spines['bottom'].set_visible(False)

	trans = mtransforms.ScaledTranslation(-20/72, 7/72, fig.dpi_scale_trans)
	ax1.text(0.0, 1.0, s="a", transform=ax1.transAxes + trans,
					fontsize='xx-large', va='center', weight="bold")

	# Robustness - TTR
	ax2 = plt.subplot(gs[:1,2:])

	get_timeseries_combined_plot_with_conf_intervals(measure="ttr", N=N)
	plt.xlabel("Year")
	plt.ylabel("Type Token Ratio")

	ax2.spines['right'].set_visible(False)
	ax2.spines['top'].set_visible(False)
	ax2.spines['bottom'].set_visible(False)

	trans = mtransforms.ScaledTranslation(-20/72, 7/72, fig.dpi_scale_trans)
	ax2.text(0.0, 1.0, s="b", transform=ax2.transAxes + trans,
					fontsize='xx-large', va='center', weight="bold")

	# Robustness - Zif
	ax3 = plt.subplot(gs[1:,2:])

	get_timeseries_combined_plot_with_conf_intervals(measure="zipf_clauset", N=N)
	plt.xlabel("Year")
	plt.ylabel("-1 x Zipf")

	ax3.invert_yaxis()
	ax3.spines['right'].set_visible(False)
	ax3.spines['top'].set_visible(False)
	ax3.spines['bottom'].set_visible(False)

	ax3.text(0.0, 1.0, s="c", transform=ax3.transAxes + trans,
					fontsize='xx-large', va='center', weight="bold")


	plt.tight_layout()


	plt.savefig("images/lexical_diversity_trend_N_{}.tiff".format(N), format="tiff", dpi=300)
	plt.savefig("images/Figure1.png", dpi=600)

	plt.show()

if __name__=="__main__":
	big_fig()