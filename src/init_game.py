from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image
from time import sleep

from LocalStorage import *

#------------------------------------------------------------------
game_width = 320
game_height = 480
game_levels = 20

out_width = 512
out_height = 768

window_size = (game_width+83, game_height+124) #320 x 480 Game area

driver_path = "./src/drivers/chromedriver"
server = "localhost:9014"
game_URL = "https://www.minijuegosgratis.com/v3/games/games/prod/219431/diamond-rush/index.html?mp_api_as3_url=https%3A%2F%2Fssl.minijuegosgratis.com%2Flechuck%2Fas3%2Flatest.swf&mp_api_as3_url_bck=https%3A%2F%2Fapi.minijuegos.com%2Flechuck%2Fclient-as%2F&mp_api_id=1951&mp_api_js_url=https%3A%2F%2Fssl.minijuegosgratis.com%2Flechuck%2Fjs%2Flatest.js&mp_api_js_url_bck=https%3A%2F%2Fapi.minijuegos.com%2Flechuck%2Fclient-js%2F&mp_assets=https%3A%2F%2Fs2.minijuegosgratis.com%2F&mp_embed=0&mp_game_id=219431&mp_game_uid=diamond-rush&mp_game_url=https%3A%2F%2Fwww.minijuegos.com%2Fembed%2Fdiamond-rush&mp_int=1&mp_locale=es_ES&mp_player_type=IFRAME&mp_site_https_url=https%3A%2F%2Fwww.minijuegos.com%2F&mp_site_name=minijuegos.com&mp_site_url=https%3A%2F%2Fwww.minijuegos.com%2F&mp_timezone=America%2FBogota&mp_view_type=&mini_signature=cd6fbd6153154338558c881412712ab8"

assets_path = "./assets/"
image_path = assets_path + "level/level.png"

#------------------------------------------------------------------
def open_game(driver, size, address, url):
	chrome_options = Options()
	chrome_options.debugger_address= address
	chrome_options.add_argument('--headless')

	browser = webdriver.Chrome(service=Service(driver), options=chrome_options)
	browser.get(url)
	browser.set_window_size(size[0],size[1])
	storage = LocalStorage(browser)
	return browser, storage

def set_level(level):
	storage.set("isNewPlayer", "false")

	for i in range(1,game_levels+1):
		storage.set("Level " + str(i), "passed")
    
	level = "Level " + str((level if level in range(1,game_levels+1) else 1))

	storage.set("levelToStart", level)
	
	game.refresh()

def generate_level_image(path):
	game_canvas = game.find_element(By.TAG_NAME, "canvas")
	game_canvas.screenshot(path)

	img = Image.open(path)
	img = img.crop((0, 0, game_width, game_height)) #Left - Top - Right - Bottom
	img = img.resize((out_width, out_height))
	img.save(path)

#------------------------------------------------------------------
game, storage = open_game(driver_path, window_size, server, game_URL)

init_level = int(input("Insert initial level: "))
set_level(init_level)

sleep(2)
generate_level_image(image_path)
