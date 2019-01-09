# bunchofutils
A bunch of python utilities. Mostly syntactic sugar for matplotlib and some simple to use threading quality of life improvements.


## Colorbar from PNG
bunchofutils allows you to extract a matplotlib.colors.LinearSegmentedColormap from a screenshot of a colorbar. You can for example turn this screen shot into a colorbar object, by runnnung: 
```python
import bunchofutils
fn = "path/to/png"
cmap = bunchofutils.colormap.colormap_from_png(fn)
```

![cororbar](https://raw.githubusercontent.com/TorbenFricke/bunchofutils/master/tests/opera_horizontal.PNG "cororbar")
