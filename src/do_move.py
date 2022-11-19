import pyautogui as py
import time
import random

#------------------------------------------------------------------
def move(x):
	py.keyDown(x)
	time.sleep(0.3)
	py.keyUp(x)

def run():
	start = random.randint(0, 3)
	if start == 0:
		move('up')
	elif start == 1:
		move('down')
	elif start == 2:
		move('right')
	elif start == 3:
		move('left')

#------------------------------------------------------------------
while True:
	run()