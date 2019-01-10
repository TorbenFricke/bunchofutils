import numpy as np
import imageio

def make_colormap(seq):
	"""
	Return a LinearSegmentedColormap

	:param seq: a sequence of floats and RGB-tuples. The floats should be increasing
	and in the interval (0,1).
	:return:
	"""
	import matplotlib.colors as mcolors
	seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
	cdict = {'red': [], 'green': [], 'blue': []}
	for i, item in enumerate(seq):
		if isinstance(item, float):
			r1, g1, b1 = seq[i - 1]
			r2, g2, b2 = seq[i + 1]
			cdict['red'].append([item, r1, r2])
			cdict['green'].append([item, g1, g2])
			cdict['blue'].append([item, b1, b2])
	return mcolors.LinearSegmentedColormap('CustomMap', cdict)


def _extract_line_from_image(im):
	"""
	Returns a line along the center of the image, along the longer side.

	:param im:
	:return:
	"""
	shape = im.shape
	if shape[0] < shape[1]:
		# horizontal screenshot
		return im[shape[0] // 2, ::-1, :3]
	else:
		# vertical screenshot
		return im[:, shape[1] // 2, :3]

def _diff(line):
	"""
	Calculates the distance between adjacent pixel. Each pixel is considered as an RGB vector and np.linalg.norm() does
	the rest

	:param line: array of RGB pixes (0..255)
	:return:
	"""
	vals = np.linalg.norm(line, axis=1)
	return np.diff(vals)

def _find_start(diff):
	"""
	Finds the end of the colorbar. Requires the background outiside the colorbar to be smooth.

	:param diff:
	:return:
	"""
	armed = False
	for i, d in enumerate(diff):
		if abs(d) > 100:
			armed = True
		if armed and abs(d) < 50:
			return i
	return 0

def _find_end(diff):
	"""
	Finds the end of the colorbar. Requires the background outiside the colorbar to be smooth.

	:param diff:
	:return:
	"""
	return len(diff) - _find_start(diff[::-1])

def _read_image(fn):
	"""
	Retunrs image data as a np array

	:param fn:
	:return:
	"""
	im = imageio.imread(fn)
	im = np.array(im)
	return im

def _trim_line(line, diff):
	"""
	Trims non colorbar pixes of a line.

	:param line:
	:param diff:
	:return:
	"""
	start = _find_start(diff)
	end = _find_end(diff)
	line = line[start:end]
	return line

def _remove_ticks(line):
	"""
	Removes tick marks from a line of pixels.

	:param line:
	:return: relative position as an array of values between 0..1; line without tick marks
	"""
	diff = _diff(line)
	pos = np.linspace(0, 1, len(line))
	pop = []
	for i, d in enumerate(diff):
		# skip last loop
		if i == len(diff) - 1:
			continue
		d_next = diff[i + 1]
		if abs(d) > 100 and abs(d_next) > 100:
			pop.append(i)
	line = np.delete(line, pop, axis=0)
	pos = np.delete(pos, pop)
	return pos, line

def reduce(pos, line, n=20):
	"""
	Picks n equidistant points along the arrays pos and line.

	:param pos:
	:param line:
	:param n:
	:return:
	"""
	assert len(pos) == len(line)
	idxs = [int(round(i / (n - 1) * (len(line) - 1))) for i in range(n)]
	return np.take(pos, idxs), np.take(line, idxs, axis=0)

def _assemble_color_seq(pos, line):
	"""
	Assembles a sequence of colordata from an array of reative positions and an array of pixels (RGB 0..255).

	:param pos:
	:param line:
	:return:
	"""
	seq = []
	for p, val, i in zip(pos, line, np.arange(len(line))):
		val = val / 255
		if i == 0:
			seq += [tuple(val)]
		elif i == len(line) - 1:
			break
		else:
			seq += [tuple(val), p, tuple(val)]
	return seq

def colormap_from_png(fn):
	"""
	Turns a screenshot of a colorbar into a matplotlib LinearSegmentedColormap. The screenshot needs to contain some
	white space around it and the colorbar needs to be roughly centered.

	:param fn: file name of screenshot
	:return: LinearSegmentedColormap
	"""
	im = _read_image(fn)
	line = _extract_line_from_image(im)
	line = list(reversed(line))
	diff = _diff(line)
	line = _trim_line(line, diff)
	pos, line = _remove_ticks(line)
	pos, line = reduce(pos, line)
	seq = _assemble_color_seq(pos, line)
	return make_colormap(seq)

def opera():
	"""
	Returns the colormap used by Opera Electromagnetic FEA Simulation Software

	:return:
	"""
	seq = [(0.3686274509803922, 0.37254901960784315, 1.0), (0.3686274509803922, 0.5333333333333333, 1.0),
	       0.05172413793103448, (0.3686274509803922, 0.5333333333333333, 1.0),
	       (0.3686274509803922, 0.6941176470588235, 1.0), 0.10344827586206896,
	       (0.3686274509803922, 0.6941176470588235, 1.0), (0.3686274509803922, 0.8627450980392157, 1.0),
	       0.15732758620689655, (0.3686274509803922, 0.8627450980392157, 1.0),
	       (0.3686274509803922, 1.0, 0.9725490196078431), 0.20905172413793102,
	       (0.3686274509803922, 1.0, 0.9725490196078431), (0.3686274509803922, 1.0, 0.8117647058823529),
	       0.2607758620689655, (0.3686274509803922, 1.0, 0.8117647058823529),
	       (0.3686274509803922, 1.0, 0.6431372549019608), 0.3146551724137931,
	       (0.3686274509803922, 1.0, 0.6431372549019608), (0.3686274509803922, 1.0, 0.4823529411764706),
	       0.36637931034482757, (0.3686274509803922, 1.0, 0.4823529411764706),
	       (0.4235294117647059, 1.0, 0.3686274509803922), 0.4202586206896552,
	       (0.4235294117647059, 1.0, 0.3686274509803922), (0.5882352941176471, 1.0, 0.3686274509803922),
	       0.47198275862068967, (0.5882352941176471, 1.0, 0.3686274509803922),
	       (0.7568627450980392, 1.0, 0.3686274509803922), 0.5258620689655172,
	       (0.7568627450980392, 1.0, 0.3686274509803922), (0.9254901960784314, 1.0, 0.3686274509803922),
	       0.5797413793103449, (0.9254901960784314, 1.0, 0.3686274509803922),
	       (1.0, 0.9137254901960784, 0.3686274509803922), 0.6314655172413793,
	       (1.0, 0.9137254901960784, 0.3686274509803922), (1.0, 0.7450980392156863, 0.3686274509803922),
	       0.6853448275862069, (1.0, 0.7450980392156863, 0.3686274509803922),
	       (1.0, 0.5843137254901961, 0.3686274509803922), 0.7370689655172413,
	       (1.0, 0.5843137254901961, 0.3686274509803922), (1.0, 0.4235294117647059, 0.3686274509803922),
	       0.7887931034482758, (1.0, 0.4235294117647059, 0.3686274509803922),
	       (1.0, 0.3686274509803922, 0.4823529411764706), 0.8426724137931034,
	       (1.0, 0.3686274509803922, 0.4823529411764706), (1.0, 0.3686274509803922, 0.6470588235294118),
	       0.8943965517241379, (1.0, 0.3686274509803922, 0.6470588235294118),
	       (1.0, 0.3686274509803922, 0.8156862745098039), 0.9482758620689655,
	       (1.0, 0.3686274509803922, 0.8156862745098039)]
	return make_colormap(seq)