import pickle
import gzip
import numpy as np
import os
from game import Visualiser, COLOR, pygame

pygame.init()
size = 5
game = Visualiser(28 * size * 10, 28 * size)


def visualize(img, weights):
    game.visualize_image(img, (0, 0), size, COLOR.alpha_map((255, 255, 255)))
    for perceptron in range(10):
        game.visualize_image(weights[:, perceptron], (28 * size * perceptron, 0), size, COLOR.weight_map(4))
    game.update()


def get_stuff():
    path = os.path.join('data', 'mnist.pkl.gz')
    with gzip.open(path, 'rb') as f:
        train_set, valid_set, test_set = pickle.load(f, encoding='latin')

    return train_set, valid_set, test_set


train_set, valid_set, test_set = get_stuff()

imgs, results = train_set
data = dict()
for img, result in zip(imgs, results):
    if result not in data:
        data[result] = []
    data[result].append(img)

weights = np.zeros([28 * 28, 10])
bias = np.zeros(10)

for img, result, idx in zip(imgs, results, range(len(imgs))):
    x = img
    z = np.dot(x, weights) + bias

    output = np.array([1 if i > 0 else 0 for i in z])  # z is a 1d array of length, loops wont affect performance

    t = np.zeros(10)
    t[result] = 1

    epsilon = 0.5

    x = np.broadcast_to(np.reshape(x, (len(x), 1)), (28 * 28, len(output)))
    weights = weights + x * (t - output) * epsilon
    bias = bias + (t - output) * epsilon

    if idx % 50 == 0:
        visualize(img, weights)
        print(idx)

visualize(img, weights)
