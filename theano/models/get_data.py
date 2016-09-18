import os
import numpy

from PIL import Image

CACHE_DIR = "../../cache/links/"

def image_to_ndarray(path):
    greyscale_image = Image.open(path).convert('L')
    return numpy.asarray(greyscale_image)
