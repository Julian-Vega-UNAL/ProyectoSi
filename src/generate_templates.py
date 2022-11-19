import cv2

templates_path = "./assets/templates/"
template_name = "TileTemplate"
format = ".png"

def rezise_and_save(img, w, h, path):
    img = cv2.resize(img, (w,h))
    cv2.imwrite(path, img)

for i in range(1,18):
    template_path = templates_path + template_name + str(i) + format
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    rezise_and_save(template, 32, 32, template_path)
