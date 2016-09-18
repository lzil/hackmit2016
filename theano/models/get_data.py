from __future__ import division

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
    all_data = [image_to_ndarray(path) for path in files]
    num_data_points = len(all_data)

    seventy_percent = num_data_points * 7 // 10
    eightyfive_percent = num_data_points * 85 // 100

    return (num_data_points[:seventy_percent],
            num_data_points[seventy_percent:eightyfive_percent]
            num_data_points[eightyfive_percent:])


def image_to_ndarray(path):
    greyscale_image = Image.open(path).convert('L')
    return numpy.asarray(greyscale_image)
