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