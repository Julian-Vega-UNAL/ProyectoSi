import pyautogui as py
import time
import random
def movimiento(x):
    py.keyDown(x)
    time.sleep(0.3)
    py.keyUp(x)
def run():
    while True:
        comienzo = random.randint(0, 3)
        if comienzo == 0:
            movimiento('up')
        elif comienzo == 1:
            movimiento('down')
        elif comienzo == 2:
            movimiento('right')
        elif comienzo == 3:
            movimiento('left')
run()