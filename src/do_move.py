import pyautogui as py
import time

#------------------------------------------------------------------
def move(x):
	py.keyDown(x)
	time.sleep(0.35) #InputLag
	py.keyUp(x)

def run(movement):
	if movement == "0":
		move('up')
	elif movement == "1":
		move('down')
	elif movement == "2":
		move('right')
	elif movement == "3":
		move('left')

#------------------------------------------------------------------
chain = "3322221111133300033111222000220000000333331112220"

time.sleep(1) #Grace time
for movement in chain:
	print(movement)
	run(movement)