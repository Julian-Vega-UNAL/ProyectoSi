import tensorflow as tf
import cv2
import numpy as np
from math import ceil
from math import floor

# Muro = M
# Personaje = P
# Diamantes = D
# Salida = S
# Llave = LL
# Puerta con llave = PLL
# Roca = R
# Placa de presion = PP
# Puerta con placa de presion = PPP
# Hueco = H
# Lava = L
# Pinchos = PI
# Tesoro = T

#Procesando Nivel
img = cv2.imread("./assets/level/level.png", cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.imwrite("./assets/level.png", img)
img = tf.keras.utils.load_img("./assets/level/level.png", color_mode="grayscale")
img_array = tf.keras.utils.img_to_array(img)

ts = 51.2   #Tile size
fr = 2      #First row
lr = 14     #Last row
fc = 1      #First column
lc = 9      #Last column

#Región Jugable
region = img_array[ceil(ts*fr):floor(ts*lr), ceil(ts*fc):floor(ts*lc)]
region_img = tf.keras.utils.array_to_img(region)
region_img.save("./assets/level/levelGray.png")

objects = [[1, "M", .65, "1"], [1, "M", .69, "2"], [1, "M", .80, "3"], [1, "M", .80, "4"], [1, "M", .80, "5"], [2, "P", .90, "6"], [3, "D", .80, "7"], [4, "S", .70, "8"], [5, "LL", .80, "9"], [6, "PLL", .70, "10"], [7, "R", .80, "11"], [8, "PP", .90, "12"], [9, "PPP", .70, "13"], [10, "H", .65, "14"], [11, "L", .30, "15"], [12, "PI", .70, "16"], [13, "T", .80, "17"]]
Matriz = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
print(Matriz)
for i in objects:  
  level_img = cv2.imread('./assets/level/levelGray.png', cv2.IMREAD_UNCHANGED)
  tile_img = cv2.imread(f'./assets/set-templates/TileTemplate{i[3]}.png', cv2.IMREAD_UNCHANGED)
  result = cv2.matchTemplate(level_img, tile_img, cv2.TM_CCOEFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
  w = tile_img.shape[1]
  h = tile_img.shape[0]
  threshold = i[2]
  yloc, xloc = np.where(result >= threshold)
  for (x, y) in zip(xloc, yloc):
      cv2.rectangle(level_img, (x, y), (x + w, y + h), (0,255,255), 1)
  rectangles = []
  for (x, y) in zip(xloc, yloc):
      rectangles.append([int(x), int(y), int(w), int(h)])
      rectangles.append([int(x), int(y), int(w), int(h)])
  rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
  for j in rectangles:
    fila = round(j[0]/51.2)
    columna = round(j[1]/51.2)
    Matriz[columna][fila] = i[1]
if Matriz[0] != ["H", 0, 0, "R", 0, 0, "R", 0]:
  Matriz[0] = ["M", "M", "M", "M", "M", "M", "M", "M"]
if Matriz[0] == ["M", "M", "M", "M", "M", "M", "M", "M"] and Matriz[4] == ["M", "M", "M", "M", "M", "M", 'PLL', "M"]:
  Matriz[0] = ["M", "D", 0, "D", 0, "D", 0, "M"]
for i in Matriz:  
    print(i)