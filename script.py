from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

import os 


##################################


#"C:\Program Files\Google\Chrome\Application\chrome.exe" -remote-debugging-port=9014 --user-data-dir="C:\Users\juanc\Desktop\WEBSCRAPING"
############



from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

print('import done')

##########################################################
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('debuggerAddress', 'localhost:9014')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x1080')
from selenium.webdriver.chrome.service import Service
#s = Service('C:\Users\juanc\Desktop\WEBSCRAPING\chromedriver.exe')
driver = webdriver.Chrome(service=Service(r"C:\Users\juanc\Desktop\SISINT\GIT\chromedriver.exe"),options=chrome_options)


print('link browser with site done')


print (driver.current_url)



driver.save_screenshot("\GIT\image.png")

#Cropiando la imagene xddddd, ajustar a donde esto se haga
im = Image.open(r"C:\Users\juanc\Desktop\SISINT\GIT\image.png")

left = 140
right = 540
top = 0
bottom = 598

im1 = im.crop((left,top,right,bottom))

newsize = (512, 768)
im1 = im1.resize(newsize)

im1.save('Level\level.png')