from PIL import Image
from pathos.multiprocessing import ProcessingPool as Pool
import os


def generate_bw_images(doc):
    images_dir = doc._images_dir
    dst = images_dir + '__images__/bw/'
    os.makedirs(dst, exist_ok=True)

    files = os.listdir(images_dir)
    files = [x for x in files if x[-3:] == 'png']

    def process(file):
        if not os.path.exists(dst + file):
            img = Image.open(images_dir + file)
            img = img.convert('RGB')
            img = img.convert('L')
            img.save(dst + file[:-4] + '.jpg')

    Pool(4).map(process, files)


def generate_jpeg_images(doc):
    images_dir = doc._images_dir
    dst = images_dir + '__images__/jpeg/'
    os.makedirs(dst, exist_ok=True)

    files = os.listdir(images_dir)
    files = [x for x in files if x[-3:] == 'png']

    def process(file):
        if not os.path.exists(dst + file):
            img = Image.open(images_dir + file)
            img = img.convert('RGB')
            img.save(dst + file[:-4] + '.jpg')

    Pool(4).map(process, files)
