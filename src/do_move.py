import pyautogui as py
import time
from calculate_path import final_path
#------------------------------------------------------------------
def move(x):
	py.keyDown(x)
	time.sleep(0.35) #InputLag
	py.keyUp(x)
	
#------------------------------------------------------------------
chain = final_path

time.sleep(5) #Grace time
for movement in chain:
	print(movement)
	move(movement)
