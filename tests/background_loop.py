import unittest
from bunchofutils import BackgroundLoop
from time import time, sleep
import gc

t0 = time()
def print_time(txt=""):
	s = ""
	if txt:
		s += "{} - ".format(txt)
	s += "{:.0f} s elapsed".format(time() - t0)
	print(s)


class TestClass(BackgroundLoop):

	@BackgroundLoop.loop(seconds=1)
	def boop(self):
		print_time("boop")

	def mop(self):
		print("mop")


class BackgroundTest(unittest.TestCase):

	def test_(self):
		test = TestClass()
		test.mop()
		sleep(3.5)
		del test