import unittest
from bunchofutils import plot, colormap
import numpy as np
import os

class PlotTest(unittest.TestCase):

	def some_plot(self, cmap):
		plt, fig, ax = plot.basic()
		N = 1000
		array_dg = np.random.uniform(0, 10, size=(N, 2))
		colors = np.random.uniform(-2, 2, size=(N,))
		plt.scatter(array_dg[:, 0], array_dg[:, 1], c=colors, cmap=cmap)
		plt.colorbar()
		plt.show()


	def test_custom_colormap(self):
		bees = colormap.make_colormap([(0, 0, 0), (1, 1, 0)])
		self.some_plot(bees)


	def test_from_png(self):
		fn = os.path.join(os.path.dirname(__file__), "opera.png")
		cmap = colormap.colormap_from_png(fn)
		self.some_plot(cmap)


	def test_from_png_horizontal(self):
		fn = os.path.join(os.path.dirname(__file__), "opera_horizontal.png")
		cmap = colormap.colormap_from_png(fn)
		self.some_plot(cmap)


	def test_from_jpeg(self):
		fn = os.path.join(os.path.dirname(__file__), "opera_horizontal.jpg")
		cmap = colormap.colormap_from_png(fn)
		self.some_plot(cmap)
