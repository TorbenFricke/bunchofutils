from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

style_dir = os.path.join(os.path.dirname(__file__), "styles")

IEEE_WIDTH = 3.6
"""Width of a ieee 2 column paper in inches"""
IEEE_HEIGHT = 1.7

def _apply_style(style="default"):
	"""
	Applies a style from styles directory in this package.

	:param style:
	:return:
	"""
	fn = os.path.join(style_dir, style + ".mplstyle")
	plt.style.use(fn)

_apply_style()

class CustomFigure(Figure):
	def __init__(self, *args, **kwargs):
		Figure.__init__(self, *args, **kwargs)

	def set_ieee_width(self):
		self.set_figwidth(IEEE_WIDTH)

	def set_ieee_size(self):
		self.set_ieee_width()
		self.set_figheight(IEEE_HEIGHT)


def _bar(arg, x_offset, width, **kwargs):
	input_kwargs = {}
	if type(arg) is tuple:
		try:
			y = arg[0]
			input_kwargs = arg[1]
		finally:
			pass
	else:
		y = arg
	kwargs.update(input_kwargs)

	n = len(y)
	x = np.linspace(0, n - 1, n) + x_offset

	plt.bar(x, y, width, **kwargs)


def bar_plot(*args, x_labels=None, width=0.8, alpha=0.5):
	"""
	Generates a bar plot

	:param args: each argument represents a plt.bar plot. Data can be provided as raw data (list or nd.array) or as a
	tuple containing both, the raw data and kwargs (data, **kwargs). Example:
	([0, 1, 2, 1, 2], {"label": "exaple"})
	:param x_labels: List of labels for the x-axis
	:param width: Width of each set of bars (default=0.8)
	:param alpha: alpha, to be applied to the color of all bars (default=0.5)
	:return:
	"""
	n = len(args)
	bar_width = width / n

	for i, arg in enumerate(args):
		x_offset = (-(n - 1) / 2 + i) / n * width
		_bar(arg, x_offset, bar_width, alpha=alpha)

	x = np.arange(len(x_labels))
	plt.xticks(x, x_labels)
	legend()



def legend(*args, **kwargs):
	"""
	Mimics the default matplotlib legend behaviour and, but adjusts the legend style.

	:param args:
	:param kwargs:
	:return:
	"""
	alpha = kwargs.pop("alpha", None)
	ax = kwargs.pop("ax", plt.gcf().gca())
	leg = ax.legend(*args, **kwargs)
	leg.get_frame().set_linewidth(0.6)
	if alpha:
		leg.get_frame().set_alpha(alpha)
	return leg


## plot configurations
def basic(*args, **kwargs):
	fig, axes = plt.subplots(*args, FigureClass=CustomFigure, **kwargs)
	return plt, fig, axes


def _ieee(*args, **kwargs):
	fig, axes = plt.subplots(*args, FigureClass=CustomFigure, **kwargs)
	fig.subplots_adjust(bottom=0.25)
	fig.set_ieee_size()
	return plt, fig, axes


def ieee(*args, **kwargs):
	_apply_style("pgf")
	mpl.use("pgf")
	return _ieee(*args, **kwargs)


def ieee_pdf(*args, **kwargs):
	_apply_style("pgf")
	set_usetex(True)
	return _ieee(*args, **kwargs)


def ieee_draft(*args, **kwargs):
	_apply_style("times")
	set_usetex(False)
	return _ieee(*args, **kwargs)


def set_colorwheel(val):
	mpl.rcParams['axes.prop_cycle'].by_key()['color'] = val

def get_colorwheel():
	return mpl.rcParams['axes.prop_cycle'].by_key()['color']

def set_usetex(val):
	mpl.rcParams['text.usetex'] = val

def get_usetex(val):
	return mpl.rcParams['text.usetex']

# explicitly "steal" some of maplotlibs funtions as a quality of live improvement. These are not overridden later.
h_line = plt.axhline
v_line = plt.axvline
show = plt.show

