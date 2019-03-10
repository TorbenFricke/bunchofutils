from bunchofutils import colormap, plot
import numpy as np

cmap = colormap.colormap_from_png("matlab.png")


plt, fig, ax = plot.basic()
N = 1000
array_dg = np.random.uniform(0, 10, size=(N, 2))
colors = np.random.uniform(-2, 2, size=(N,))
plt.scatter(array_dg[:, 0], array_dg[:, 1], c=colors, cmap=cmap)
plt.colorbar()
plt.show()