# pip install Pillow
from PIL import Image  # Python Image Library - Image Processing
import glob
import sys
import os

imagesDirectory = ''
if len(sys.argv) > 1:
    imagesDirectory = sys.argv[1]
else:
    imagesDirectory = input("Please enter image(s) directory: ")

files = glob.glob(os.path.join(imagesDirectory, "*.png"))

print("Searching for pngs...")

if len(files) == 0:
    sys.exit("Error: Image directory provided does not contain png files")

print("Pngs found, creating jpgs...")

# based on SO Answer: https://stackoverflow.com/a/43258974/5086335
for file in files:
    im = Image.open(file)
    rbg_im = im.convert('RGB')
    rbg_im.save(file.replace("png", "jpg"), quality=95)
    print(os.path.basename(file) + " processed")

print("Process complete!")
