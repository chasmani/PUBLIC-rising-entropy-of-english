
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np

from design_scheme import LINEWIDTH, COLOR_MAG, COLOR_FIC, COLOR_4, COLOR_BLACK, FONT_PROP


def plot_discrete_info_curve(prevalence=1, handling_time=1, q=1, n=3, color="red", size_ratio=1):

	current_time = 0
	current_u = 0

	r = q/handling_time

	for i in range(n):

		encounter_time = current_time + 1/prevalence
		finish_time = encounter_time + handling_time

		tt_wait = np.linspace(current_time, encounter_time, 100)
		uu_wait = [current_u] * 100

		plt.plot(tt_wait, uu_wait, color=color, linewidth=LINEWIDTH*size_ratio)

		tt_handle = np.linspace(encounter_time, finish_time, 100)
		uu_handle = current_u + (tt_handle - encounter_time)*r

		plt.plot(tt_handle, uu_handle, color=color, linewidth=LINEWIDTH*size_ratio)

		current_time = finish_time
		current_u += q

	encounter_time = current_time + 1/prevalence
	finish_time = encounter_time + handling_time

	tt_wait = np.linspace(current_time, encounter_time, 100)
	uu_wait = [current_u] * 100	

	plt.plot(tt_wait, uu_wait, color=color, linewidth=LINEWIDTH)


def plot_expected_patch_utility(prevalence=1, handling_time=1, q=1, n=3, color="red", size_ratio=1):

	R = q/(1/prevalence + handling_time)

	tt_max = (1/prevalence + handling_time)*n

	tt = np.linspace(0, tt_max, 100)
	uu = R*tt
	plt.plot(tt, uu, color=color, linestyle="dashed", linewidth=LINEWIDTH*size_ratio)



def get_geometry_plot():

	plt.ylabel("Utility")

	xtick_marks = ['']*30
	xtick_marks[10] = r"$\frac{1}{\lambda_m}$"
	xtick_marks[20] = r"$\frac{1}{\lambda_m} + \bar{t}_m$"
	#xtick_marks[20] = r"$t_h"


	ytick_marks = ['']*22
	ytick_marks[10] = r"$\bar{u}_m$"

	plt.xticks(np.arange(0,3,0.1), xtick_marks)
	plt.yticks(np.arange(0,2.2,0.1), ytick_marks)
	
	ax = plt.gca()
	ax.tick_params(axis=u'both', which=u'both',length=0)

	plt.ylim(0,2.2)
	plt.xlim(0,4.5)
	plt.xlabel("Time")
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	prevalence=1
	handling_time=1 
	q=1
	n=2
	color=COLOR_BLACK

	plt.axvline(x=2, ymax=1/2.2, color="lightgray", linewidth=LINEWIDTH)
	plt.axhline(y=1, xmax=2/4.5, color="lightgray", linewidth=LINEWIDTH)

	plot_expected_patch_utility(prevalence=prevalence, handling_time=handling_time, q=q, n=n, color=color, size_ratio=2)
	plot_discrete_info_curve(prevalence=prevalence, handling_time=handling_time, q=q, n=n, color=color, size_ratio=2)

	plt.plot(0,0, color=COLOR_BLACK, label=r"Cumulative Utility")
	plt.plot(0,0, color=COLOR_BLACK, linestyle="dashed", label=r"Utility Rate")
	



	plt.annotate(r"$\bar{r}_m$", (1.6,0.4))




def plot_short_vs_long_low_prevalence():

	prevalence = 0.4
	xlim_right = 8

	AXES_COLOR = "lightgray"
	plt.xticks([])
	plt.yticks([])

	ax = plt.gca()
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)

	plot_discrete_info_curve(prevalence=prevalence, handling_time=5, q=3, n=1, color=COLOR_FIC, size_ratio=2)
	plot_expected_patch_utility(prevalence=prevalence, handling_time=5, q=3, n=1, color=COLOR_FIC, size_ratio=2)

	plot_discrete_info_curve(prevalence=prevalence, handling_time=0.7, q=1, n=3, color=COLOR_MAG, size_ratio=2)
	plot_expected_patch_utility(prevalence=prevalence, handling_time=0.7, q=1, n=3, color=COLOR_MAG, size_ratio=2)

	plt.xlim(left=0, right=xlim_right)
	plt.ylim(bottom=0)

	plt.plot([],[], color=COLOR_FIC, label="Long-form")
	plt.plot([],[], color=COLOR_MAG, label="Short-form")

	plt.legend()



def plot_media_category_differences():


	AXES_COLOR = "lightgray"


	plt.xticks([])
	plt.yticks([])

	ax = plt.gca()
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)



	plot_discrete_info_curve(prevalence=1, handling_time=5, q=3, n=1, color=COLOR_FIC, size_ratio=2)
	#plot_expected_patch_utility(prevalence=1, handling_time=5, q=3, n=1, color=COLOR_FIC)

	plot_discrete_info_curve(prevalence=1, handling_time=1, q=1, n=3, color=COLOR_MAG, size_ratio=2)

	plot_expected_patch_utility(prevalence=1, handling_time=1, q=1, n=3, color="silver", size_ratio=2)


	plt.plot(0,0,color=COLOR_FIC, label="Long-form")
	plt.plot(0,0,color=COLOR_MAG, label="Short-form")


	plt.xlim(left=0, right=8)
	plt.ylim(bottom=0)


def plot_model_low_and_high_prevalence():

	fig = plt.figure()

	fig_width, fig_height = plt.gcf().get_size_inches()

	fig = plt.figure(figsize=(fig_width*2, fig_height), constrained_layout=True)
	
	trans = mtransforms.ScaledTranslation(-20/72, 7/72, fig.dpi_scale_trans)

		# Model General
	ax1 = fig.add_subplot(131)

	get_geometry_plot()
	plt.legend()
	plt.title("Model")

	ax1.text(0.0, 1.0, s="a", transform=ax1.transAxes + trans,
					fontsize='xx-large', va='center', weight="bold")


	ax2 = fig.add_subplot(132)
	plot_short_vs_long_low_prevalence()
	plt.title(r"Low Prevalance, $\lambda$")
	plt.ylabel("Utility")
	plt.xlabel("Time")

	ax2.text(0.0, 1.0, s="b", transform=ax2.transAxes + trans,
					fontsize='xx-large', va='center', weight="bold")


	ax3 = fig.add_subplot(133)

	plot_media_category_differences()
	plt.title(r"High Prevalance, $\lambda$")
	plt.ylabel("Utility")
	plt.xlabel("Time")

	ax3.text(0.0, 1.0, s="c", transform=ax3.transAxes + trans,
					fontsize='xx-large', va='center', weight="bold")


	plt.savefig("images/media_patch_model.tiff", dpi=300)

	plt.show()


if __name__=="__main__":
	plot_model_low_and_high_prevalence()