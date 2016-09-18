from __future__ import division

from six.moves import urllib
import glob, os

import uuid

from PIL import Image

def make_square_thumbnail(filename, thumbnail_size, outdir):
    dirname, basename = os.path.split(filename)
    basebasename, _ = os.path.splitext(basename)

    im = Image.open(filename)
    im_width, im_height = im.size
    im_min_dimension = min(im.size)

    left = (im_width - im_min_dimension) // 2
    top = (im_height - im_min_dimension) // 2
    cropped_image = im.crop(
        (left, top, left + im_min_dimension, top + im_min_dimension))
    cropped_image.thumbnail((thumbnail_size, thumbnail_size))
    try:
        cropped_image.save(os.path.join(outdir, basebasename + "_thumbnail.jpg"), "JPEG")
    except IOError:
        cropped_image.convert('RGB').save(os.path.join(outdir, basebasename + "_thumbnail.jpg"))

i = 0
for filename in os.listdir("tmp/downloaded-pusheen"):
    if filename.endswith(".jpg"):
        print(str(i) + ". " + filename)
        try:
            make_square_thumbnail("tmp/downloaded-pusheen/" + filename, 128, "thumbnails-pusheen")
            i += 1
        except:
            continue

