from __future__ import division, print_function

import os
import numpy
import random

from PIL import Image

CACHE_DIR = "../../cache/links/"


def directory_to_dataset(dirname, permute=True):
    # check precondition
    assert(os.path.isdir(dirname))

    files = os.listdir(dirname)
    if permute:
        random.shuffle(files)
    all_data = [image_to_ndarray(os.path.join(dirname, path)).flatten() for path in files]
    num_data_points = len(all_data)

    train_frac = num_data_points * 70 // 100
    non_test_frac = num_data_points * 85 // 100

    # sanity checks
    assert(train_frac < non_test_frac)
    assert(non_test_frac < num_data_points)

    # train 70, validate 15, test 15
    return (numpy.asarray(all_data[:train_frac]),
            numpy.asarray(all_data[train_frac:non_test_frac]),
            numpy.asarray(all_data[non_test_frac:]))


def image_to_ndarray(path):
    greyscale_image = Image.open(path).convert('L')
    return numpy.asarray(greyscale_image)
