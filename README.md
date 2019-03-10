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

## Background Loop

Sometimes, all you need in life is for a function (say a bit of housekeeping) to run periodically. If you do not need 
precise timing of fine grained control, the *BackgroundLoop* base class may be for you.

Just use the ```@BackgroundLoop.loop(seconds=1)``` function decorator to have a method run periodically. The minimum 
interval is one second. If your needs are more complex, take a look at http://www.celeryproject.org/.

```python
from bunchofutils import BackgroundLoop
from time import sleep

class LoopTestClass(BackgroundLoop):
	def __init__(self):
		# do some stuff here,
		# but be sure to initialize super class!
		BackgroundLoop.__init__(self)

	@BackgroundLoop.loop(seconds=1)
	def boop(self):
		print("boop")

	@BackgroundLoop.loop(seconds=2)
	def beep(self):
		print("beep")


loop_test = LoopTestClass()
sleep(3.1)
```
Output:
```
boop
beep
boop
boop

Process finished with exit code 0
```



### Caveats

Each Background loop class spawns exatly one thread to periodically run the functions. This background thread executes 
all loop methods, up for execution and sleeps for one second afterwards. If for example, one loop method takes 3 seconds 
to execute, all other methods are delayed by 3 seconds. 

Here is the actual implementation - sophisticated, I know :D

```python
if not self.loop_functions:
    return
while True:
    sleep(1)
    # make sure parent is still alive
    if not self.parent():
        return
    self._i += 1
    for f in self.loop_functions:
        if self._i % f.interval != 0:
            continue
        try:
            f()
        except Exception as e:
            print("encountered exception in background loop: {}".format(e))
```

tl;dr: Do not use ```BackgroundLoop``` for anything timing sensitive.
