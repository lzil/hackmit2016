from __future__ import division, print_function

import os
import numpy
import random

import theano
from PIL import Image

CACHE_DIR = "../../cache/"
negative_dir = os.path.join(CACHE_DIR, "thumbnails", "_negative")


def append_labels(data, label):
    return (data, numpy.ones(len(data)) * label)


def directory_to_dataset(dirname):
    # check precondition
    assert(os.path.isdir(dirname))

    positive_files = [(os.path.join(dirname, basename), 1) for basename in os.listdir(dirname)]
    negative_files = [(os.path.join(negative_dir, basename), 0) for basename in os.listdir(negative_dir)]
    files = positive_files + negative_files
    random.shuffle(files)

    all_data = [(image_to_ndarray(path).flatten(), label) for (path, label) in files]
    num_data_points = len(all_data)

    train_frac = num_data_points * 70 // 100
    non_test_frac = num_data_points * 85 // 100

    # sanity checks
    assert(train_frac < non_test_frac)
    assert(non_test_frac < num_data_points)

    # train 70, validate 15, test 15
    def transpose(labeled_data):
        (data, labels) = zip(*labeled_data)
        return (theano.shared(numpy.asarray(data,dtype='float32')),
            theano.tensor.cast(theano.shared(numpy.asarray(labels)), 'int32'))

    return tuple(map(transpose,
        [all_data[:train_frac], all_data[train_frac:non_test_frac], all_data[non_test_frac:]]
        ))

def image_to_ndarray(path):
    greyscale_image = Image.open(path).convert('L')
    return numpy.asarray(greyscale_image)
