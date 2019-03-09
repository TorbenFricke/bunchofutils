import unittest
from bunchofutils import BackgroundLoop
from time import time, sleep
import gc


_has_gone_boom = False

class LoopTestClass(BackgroundLoop):
	def __init__(self, verbose=True):
		self.lines = []
		self.t0 = time()
		self.verbose = verbose
		# be sure, to initialize super class!
		BackgroundLoop.__init__(self)

	def print_time(self, txt=""):
		s = ""
		if txt:
			s += "{} - ".format(txt)
		s += "{:.1f} s elapsed".format(time() - self.t0)
		if self.verbose:
			print(s)
		self.lines.append(s)

class BoopTestClass(LoopTestClass):

	@BackgroundLoop.loop(seconds=1)
	def boop(self):
		self.print_time("boop")

	@BackgroundLoop.loop(seconds=3)
	def beep(self, txt=""):
		self.print_time("beep started" + txt)
		sleep(.2)
		self.print_time("beep ended" + txt)

	@BackgroundLoop.loop(seconds=8)
	def boom(self):
		global _has_gone_boom
		_has_gone_boom = True


class BackgroundTest(unittest.TestCase):

	def test_execution_order(self):
		test = BoopTestClass()
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
		# delete class
		del test

		# will raise an error, if the Background loop continues to run.
		sleep(2)
		self.assertFalse(_has_gone_boom)
