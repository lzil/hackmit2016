from __future__ import division, print_function

import os
import numpy
import random

from PIL import Image

CACHE_DIR = "../../cache/links/"


def directory_to_dataset(dirname, permute=True):
    assert(os.path.isdir(dirname))
    files = os.listdir(dirname)
    if permute:
        random.shuffle(files)
    all_data = [image_to_ndarray(os.path.join(dirname, path)).flatten() for path in files]
    num_data_points = len(all_data)

    seventy_percent = num_data_points * 70 // 100
    eightyfive_percent = num_data_points * 85 // 100

    return (numpy.asarray(all_data[:seventy_percent]),
            numpy.asarray(all_data[seventy_percent:eightyfive_percent]),
            numpy.asarray(all_data[eightyfive_percent:]))


def image_to_ndarray(path):
    greyscale_image = Image.open(path).convert('L')
    return numpy.asarray(greyscale_image)
