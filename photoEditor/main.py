from PIL import Image, ImageEnhance, ImageFilter
import os
from sys import argv

path = "./imgs"
pathtOut = "/editedImgs"
contrast = argv[1] if len(argv) > 1 else '.'

for filename in os.listdir(path):
    img = Image.open(f"{path}/{filename}")

    edit = img.filter(ImageFilter.SHARPEN).convert('L')
    if contrast and contrast == "-c":
        factor = 1.5
        enhancer = ImageEnhance.Contrast(edit)
        edit = enhancer.enhance(factor)

    clean_name = os.path.splitext(filename)[0]

    edit.save(f".{pathtOut}/{clean_name}_edited.jpg")

