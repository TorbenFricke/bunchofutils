import unittest
from bunchofutils import BackgroundLoop
from tests.background_loop import LoopTestClass
from time import time, sleep
import pickle



_has_gone_boom = False


class PickleTestClass(LoopTestClass):

	@BackgroundLoop.loop(seconds=1)
	def boop(self):
		self.print_time("boop")

	@BackgroundLoop.loop(seconds=5)
	def boom(self):
		global _has_gone_boom
		_has_gone_boom = True


class BackgroundTest(unittest.TestCase):

	def test_pickling(self):
		test = PickleTestClass()
		sleep(1.2)

		# pickle and unpickle
		s = pickle.dumps(test)
		del test
		sleep(.3)
		test = pickle.loads(s)
		sleep(3.1)
		test.boop()
		lines = ['boop - 1.0 s elapsed',
		         'boop - 2.5 s elapsed',
		         'boop - 3.5 s elapsed',
		         'boop - 4.5 s elapsed',
		         'boop - 4.6 s elapsed']

		for l1, l2 in zip(test.lines, lines):
			self.assertEqual(l1, l2)

		del test

		# will raise an error, if the Background loop continues to run.
		sleep(2)
		self.assertFalse(_has_gone_boom)

