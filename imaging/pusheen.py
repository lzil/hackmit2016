#basically a copy of thumbnail.py

from __future__ import division

from six.moves import urllib
import glob, os

import uuid

from PIL import Image


temp_dir = "tmp/downloaded-pusheen"
def mkdir_if_not_exist(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

mkdir_if_not_exist(temp_dir)
mkdir_if_not_exist("thumbnails-pusheen")


def download_image(url):
    print("downloading " + url)
    random_hash = uuid.uuid4().hex
    filename = url.split("/")[-1]
    download_path = os.path.join(temp_dir, random_hash + ".jpg")
    try:
        urllib.request.urlretrieve(url, download_path)
        return download_path
    except:
        print("   failed to download " + url)
        return None
    #return download_path


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


def download_and_thumbnail(file_object, size):
    paths = [download_image(url) for url in file_object]
    for path in paths:
        make_square_thumbnail(path, size, "thumbnails")

# for filename in glob.glob("/Users/txz/Pictures/happiness/*.jpg"):
#     abspath = os.path.join("/Users/txz/Pictures/happiness", filename)
#     with open(filename, 'r') as f:
#         make_square_thumbnail(abspath, 128, "thumbnails")

with open("../cache/links/pusheen-big.txt", 'r') as f:
    paths = [download_image(url) for url in f]
    i = 0
    for path in paths:
        print(i)
        print("making thumbnail " + path)
        if path == None:
            continue
        make_square_thumbnail(path, 128, "thumbnails-pusheen")
        i += 1
