from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image
from time import sleep

from LocalStorage import *

#------------------------------------------------------------------
#map_tiles = (15,10) #Rows and Columns
#tile_size = (64, 64) #Pixels
window_size = (403, 604) #320 x 480 Game area

driverPath = "./src/drivers/chromedriver"
server = "localhost:9014"
gameURL = "https://www.minijuegosgratis.com/v3/games/games/prod/219431/diamond-rush/index.html?mp_api_as3_url=https%3A%2F%2Fssl.minijuegosgratis.com%2Flechuck%2Fas3%2Flatest.swf&mp_api_as3_url_bck=https%3A%2F%2Fapi.minijuegos.com%2Flechuck%2Fclient-as%2F&mp_api_id=1951&mp_api_js_url=https%3A%2F%2Fssl.minijuegosgratis.com%2Flechuck%2Fjs%2Flatest.js&mp_api_js_url_bck=https%3A%2F%2Fapi.minijuegos.com%2Flechuck%2Fclient-js%2F&mp_assets=https%3A%2F%2Fs2.minijuegosgratis.com%2F&mp_embed=0&mp_game_id=219431&mp_game_uid=diamond-rush&mp_game_url=https%3A%2F%2Fwww.minijuegos.com%2Fembed%2Fdiamond-rush&mp_int=1&mp_locale=es_ES&mp_player_type=IFRAME&mp_site_https_url=https%3A%2F%2Fwww.minijuegos.com%2F&mp_site_name=minijuegos.com&mp_site_url=https%3A%2F%2Fwww.minijuegos.com%2F&mp_timezone=America%2FBogota&mp_view_type=&mini_signature=cd6fbd6153154338558c881412712ab8"

assetsPath = "./assets/"
imagePath = assetsPath + 'level/level.png'

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

    for i in range(1,20):
        storage.set("Level " + str(i), "passed")
    
    level = "Level " + str((level if level in range(1,20) else 1))

    storage.set("levelToStart", level)

    game.refresh()

def generate_level_image(path):
    game_canvas = game.find_element(By.TAG_NAME, "canvas")
    game_canvas.screenshot(path)

    img = Image.open(path)
    img = img.crop((0, 0, 320, 480)) #Left - Top - Right - Bottom
    img.save(path)

#------------------------------------------------------------------
game, storage = open_game(driverPath, window_size, server, gameURL)

init_level = int(input("Insert initial level: "))
set_level(init_level)

sleep(2)
generate_level_image(imagePath)
#------------------------------------------------------------------
