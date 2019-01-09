import unittest
from bunchofutils import plot
import numpy as np

class PlotTest(unittest.TestCase):
	do_not_show = True

	def show(self):
		"""
		Either shows the plot, or reloads torbotils and matplotlib to reset
		:return:
		"""
		plot.show()


	def test_visually(self):
		plt, fig, ax = plot.basic()
		plt.plot([1, 2, 4], label="test")
		plt.plot([2, 2, 3], label="test2")
		plot.h_line(1, color="red")
		plot.legend(loc="lower right", alpha=1.)
		plt.xlabel("x-axis")
		plt.ylabel("y-axis")
		self.show()

	def test_tex_visually(self):
		plt, fig, ax = plot.ieee_pdf()
		plt.plot([1, 2, 4], label="test")
		plot.legend(loc="lower right")
		plt.xlabel("x-axis")
		plt.ylabel("y-axis")
		self.show()


	def test_bar_visually(self):
		plt, fig, ax = plot.basic()
		b1 = [0.0022312583236333053, 2.30072232554551e-05, 2.0288252517587813e-05, 1.0155657023897475e-05,
		       1.3928905164667381e-05, 5.789764361632152e-06, 1.2345582129869121e-05, 1.125099009374256e-05,
		       8.375211416428887e-06, 8.835039982342082e-06]
		b2 = [0.042499270794620105, 5.264903451938897e-05, 0.0019489462821535033, 4.024229907858245e-05,
		         3.077925332007259e-05, 3.093287138100361e-05, 0.00014016427496842322, 1.853694957102855e-05,
		         2.3703962751812195e-05, 5.536745197248537e-06]
		b3 = [0.023030640797494107, 1.5970049271846566e-05, 0.000811411992130343, 1.2886894992963836e-05,
		           1.0031007849522452e-05, 8.636313098929208e-06, 5.124210336705097e-05, 7.615945200570969e-06,
		           1.2259974414554043e-05, 5.353390492722848e-06]
		b4 = [0.0020611468530092264, 5.413584591167569e-06, 1.5629098646494706e-05, 5.0767580016579335e-06,
		       6.593670459802336e-06, 3.9572836668542565e-06, 7.1269968357244615e-06, 6.5854090982057785e-06,
		       9.375832865607904e-06, 3.4312823489133688e-06]

		plot.bar_plot((b1, {"label": "bar 1"}),
		              (b2, {"label": "bar 2"}),
		              (b3, {"label": "bar 3"}),
		              (b4, {"label": "bar 4"}),
		              x_labels=["1st", "2nd", "3rd"] + ["{}th".format(i+1) for i in range(3, len(b1))])
		self.show()


	def test_ieee_draft_visually(self):
		plt, fig, ax = plot.ieee_draft()
		plt.plot([1, 2, 4], label="test")
		plot.legend(loc="lower right")
		plt.xlabel("x-axis")
		plt.ylabel("y-axis")
		self.show()


	def test_font_in_pgf(self):
		plt, fig, ax = plot.ieee()
		plt.plot([1, 2, 4], label="test")
		plot.legend(loc="lower right")
		fn = "test_font_in_pgf.pgf"
		plt.savefig(fn)
		with open(fn) as f:
			s = f.read()
		assert not r"}\setmainfont{" in s

