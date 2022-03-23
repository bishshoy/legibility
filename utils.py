from PIL import Image, ImageDraw, ImageFont
import os

def generate_blank_images(doc):
    images_dir = doc._images_dir
    dst = images_dir+'blank/'
    files = os.listdir(images_dir)
    files = [x for x in files if x[-3:] == 'png']
    os.makedirs(dst, exist_ok=True)
    for file in files:
        if not os.path.exists(dst + file):
            blank_out_image(images_dir, dst, file)


def blank_out_image(src, dst, filename):
    img = Image.open(src + filename).convert('L')
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (img.width, img.height)], fill='white', outline='black', width=img.width//50)
    font = ImageFont.truetype('Arial.ttf', img.width // 20)
    draw.text((2*img.width//12, 4*img.height//12), filename, font=font, fill='black')
    draw.text((2*img.width//12, 6*img.height//12), str(img.height)+' x '+str(img.width), font=font, fill='black')
    img.save(dst + filename)