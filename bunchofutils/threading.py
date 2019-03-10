import threading, types
from functools import wraps
from time import sleep, time
from weakref import WeakMethod, ref


class loop_function(object):
	def __init__(self, func, interval: int=1, parent=None):
		if not callable(func):
			raise TypeError("input function not callable")
		self._func = func
		self._parent = None
		self.interval = int(interval)

	def set_parent(self, parent):
		self._parent = ref(parent)

	def __str__(self):
		return "{} @ {} s interval".format(self._func, self.interval)

	def __call__(self, *args, **kwargs):
		self._func(self._parent(), *args, **kwargs)


class _MainLoopThread(threading.Thread):
	def __init__(self, functions, parent):
		threading.Thread.__init__(self)
		self._i = 0
		self.loop_functions = functions
		self.daemon = True
		self.parent = ref(parent)

	def run(self):
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


class BackgroundLoop(object):
	"""
	Super class, featuring the @loop decorator for functions to be run regularly.
	"""
	def __init__(self):
		_loop_functions = []
		# reflect and find loop functions
		for attr in dir(self):
			try:
				attr = self.__getattribute__(attr)
			except:
				continue
			if isinstance(attr, loop_function):
				attr.set_parent(self)
				# remember loop function
				_loop_functions.append(attr)
		self._background_loop = _MainLoopThread(_loop_functions, self)
		self._background_loop.start()


	@staticmethod
	def loop(seconds=0., minutes=0., hours=0., days=0.):
		# calculate interval in seconds
		interval = seconds + minutes * 60 + hours * 60 * 60 + days * 60 * 60 * 24
		# default interval is one minute
		if interval == 0:
			interval = 60

		def wrapper(f):
			loop_func = loop_function(f, interval)
			return loop_func

		return wrapper


	# pickle
	def __getstate__(self):
		ret = {}
		for key, val in self.__dict__.items():
			if isinstance(val, loop_function):
				continue
			if key in ["_loop_functions", "_background_loop"]:
				continue
			ret[key] = val

		return ret


	def __setstate__(self, state):
		BackgroundLoop.__init__(self)
		self.__dict__.update(state)

