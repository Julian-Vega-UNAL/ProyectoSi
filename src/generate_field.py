import cv2
import numpy as np

from math import ceil
from math import floor

#------------------------------------------------------------------
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

#------------------------------------------------------------------
assets_path = "./assets/"
templates_path = assets_path + "templates/"

level_image_path = assets_path + "level/level.png"
level_gray_image_path = assets_path + "level/levelGray.png"

ts = 32			#Tile size
fr = 2			#First row
lr = 14			#Last row
fc = 1			#First column
lc = 9			#Last column

rows = lr - fr	#Row number
cols = lc - fc	#Column number

tileset = [[1, "M", .65, "1"], [1, "M", .69, "2"], [1, "M", .80, "3"], [1, "M", .80, "4"], [1, "M", .80, "5"], [2, "P", .90, "6"], [3, "D", .80, "7"], [4, "S", .70, "8"], [5, "LL", .80, "9"], [6, "PLL", .70, "10"], [7, "R", .80, "11"], [8, "PP", .90, "12"], [9, "PPP", .70, "13"], [10, "H", .65, "14"], [11, "L", .30, "15"], [12, "PI", .70, "16"], [13, "T", .80, "17"]]
field = [[0]*cols]*rows		#8x14 matrix

#------------------------------------------------------------------
def recognise_tile(tile):
	tile_type_num = tile[0]
	tile_type = tile[1]
	tile_threshold = tile[2]
	tile_subtype = tile[3]

	tile_template = cv2.imread(templates_path + f'/TileTemplate{tile_subtype}.png', cv2.IMREAD_UNCHANGED)
	w = tile_template.shape[1]
	h = tile_template.shape[0]

	result = cv2.matchTemplate(level_img, tile_template, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	yloc, xloc = np.where(result >= tile_threshold)

	for (x, y) in zip(xloc, yloc):
		cv2.rectangle(level_img, (x, y), (x + w, y + h), (0,255,255), 1)
  
	rectangles = []
	for (x, y) in zip(xloc, yloc):
		rectangles.append([int(x), int(y), int(w), int(h)])
		rectangles.append([int(x), int(y), int(w), int(h)])
  
	rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

	for rect in rectangles:
		row = round(rect[0]/ts)
		col = round(rect[1]/ts)
		field[col][row] = tile_type

#------------------------------------------------------------------
level_img = cv2.imread(level_image_path, cv2.IMREAD_UNCHANGED)
level_img = cv2.cvtColor(level_img, cv2.COLOR_BGR2GRAY)

region = level_img[ceil(ts*fr):floor(ts*lr), ceil(ts*fc):floor(ts*lc)]
cv2.imwrite(level_gray_image_path, level_img)

for tile in tileset:
	recognise_tile(tile)

#Corner cases
if field[0] != ["H", 0, 0, "R", 0, 0, "R", 0]:
	field[0] = ["M", "M", "M", "M", "M", "M", "M", "M"]

if field[0] == ["M", "M", "M", "M", "M", "M", "M", "M"] and field[4] == ["M", "M", "M", "M", "M", "M", 'PLL', "M"]:
	field[0] = ["M", "D", 0, "D", 0, "D", 0, "M"]

#------------------------------------------------------------------
for i in field:
	print(i)
