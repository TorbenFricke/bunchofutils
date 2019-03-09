import unittest
from bunchofutils import BackgroundLoop
from time import time, sleep
import gc


verbose = True

class TestClass(BackgroundLoop):
	def __init__(self):
		self.lines = []
		self.t0 = time()
		# be sure, to initialize super class!
		BackgroundLoop.__init__(self)

	def print_time(self, txt=""):
		s = ""
		if txt:
			s += "{} - ".format(txt)
		s += "{:.1f} s elapsed".format(time() - self.t0)
		if verbose:
			print(s)
		self.lines.append(s)


	@BackgroundLoop.loop(seconds=1)
	def boop(self):
		self.print_time("boop")

	@BackgroundLoop.loop(seconds=3)
	def beep(self, txt=""):
		self.print_time("beep started" + txt)
		sleep(.2)
		self.print_time("beep ended" + txt)


class BackgroundTest(unittest.TestCase):

	def test_(self):
		test = TestClass()
		sleep(.5)
		# calling function manually
		test.boop()
		test.beep(" - manually called")
		sleep(7)
		lines = ['boop - 0.5 s elapsed',
		         'beep started - manually called - 0.5 s elapsed',
		         'beep ended - manually called - 0.7 s elapsed', 'boop - 1.0 s elapsed', 'boop - 2.0 s elapsed',
		         'beep started - 3.0 s elapsed', 'beep ended - 3.2 s elapsed', 'boop - 3.2 s elapsed',
		         'boop - 4.2 s elapsed',
		         'boop - 5.2 s elapsed', 'beep started - 6.2 s elapsed', 'beep ended - 6.4 s elapsed',
		         'boop - 6.4 s elapsed',
		         'boop - 7.4 s elapsed']
		for l1, l2 in zip(test.lines, lines):
			self.assertEqual(l1, l2)

		del test