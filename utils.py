from PIL import Image, ImageDraw, ImageFont
import os


def generate_blank_images(doc):
    images_dir = doc._images_dir
    dst = images_dir + '__images__/'
    files = os.listdir(images_dir)
    files = [x for x in files if x[-3:] == 'png']
    os.makedirs(dst, exist_ok=True)
    for file in files:
        if not os.path.exists(dst + file):
            blank_out_image(images_dir, dst, file)


def blank_out_image(src, dst, filename):
    img = Image.open(src + filename).convert('L')
    img.save(dst + filename)
