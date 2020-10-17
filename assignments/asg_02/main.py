import pickle
import gzip
import numpy
import os


def get_stuff():
    path = os.path.join('data', 'mnist.pkl.gz')
    with gzip.open(path, 'rb') as f:
        train_set, valid_set, test_set = pickle.load(f, encoding='latin')

    return train_set, valid_set, test_set
