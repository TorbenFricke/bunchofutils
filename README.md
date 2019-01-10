# bunchofutils
A bunch of python utilities. Mostly syntactic sugar for matplotlib and some simple to use threading quality of life 
improvements.


## Colorbar from PNG
bunchofutils allows you to extract a matplotlib.colors.LinearSegmentedColormap from a screenshot of a colorbar. You can
for example turn this screen shot
 
![cororbar](https://raw.githubusercontent.com/TorbenFricke/bunchofutils/master/tests/opera_horizontal.PNG "cororbar")

into a colorbar object, by running: 
```python
import bunchofutils
fn = "path/to/png"
cmap = bunchofutils.colormap.colormap_from_png(fn)
```

## Plotting

bunchofutils sets up matplotlib for use in ieee papers. The backend is switched to pgf, the font is removed from the pgf
output file, colors and font sizes are adjusted. 
```python
import bunchofutils
plt, fig, ax = bunchofutils.plot.ieee()
```
A draft mode does not switch the backend and sets the font to Times to get a rough idea of what the end result might 
look like.
```python
import bunchofutils
plt, fig, ax = bunchofutils.plot.ieee_draft()
plt.plot([1, 3, 5, 2], label="some line")
bunchofutils.plot.legend() # adjusts legend frame. This did not work using rcparams
plt.show()

```