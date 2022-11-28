import pyautogui as py
import time
from init_game import game
from calculate_path import final_path
#------------------------------------------------------------------
def move(x):
	py.keyDown(x)
	time.sleep(0.3) #InputLag
	py.keyUp(x)
	
#------------------------------------------------------------------
browser = game
chain = final_path
print(chain)
print("GO TO BROWSER!")
time.sleep(2) #Grace time
for movement in chain:
	move(movement)
time.sleep(5)
browser.close()