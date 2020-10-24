import pickle
import gzip
import numpy as np
import os
from game import Visualiser, COLOR, pygame

pygame.init()


class Layer:
    def __init__(self):
        self.weights = np.zeros([28 * 28, 10])
        self.bias = np.zeros(10)
        self.delta = 0.6
        self.size_on_screen = 4
        self.game = Visualiser(28 * self.size_on_screen * 10, 28 * self.size_on_screen)
        self.view_progress = True
        path = os.path.join('data', 'mnist.pkl.gz')
        with gzip.open(path, 'rb') as f:
            self.train_set, self.valid_set, self.test_set = pickle.load(f, encoding='latin')

    def visualize(self):
        # self.game.visualize_image(img, (0, 0), self.size_on_screen, COLOR.alpha_map((255, 255, 255)))
        for perceptron in range(10):
            self.game.visualize_image(self.weights[:, perceptron], (28 * self.size_on_screen * perceptron, 0),
                                      self.size_on_screen, COLOR.weight_map(4))
        self.game.update()

    def train(self):
        images, results = self.train_set
        iterations = len(images)

        for img, result, idx in zip(images, results, range(iterations)):
            x = img
            z = np.dot(x, self.weights) + self.bias
            
            # z is a 1d array of length, loops wont affect performance
            output = np.array( [1 if i > 0 else 0 for i in z])

            t = np.zeros(10)
            t[result] = 1

            x = np.broadcast_to(np.reshape(x, (len(x), 1)), (28 * 28, len(output)))
            self.weights = self.weights + x * (t - output) * self.delta
            self.bias = self.bias + (t - output) * self.delta

            if idx % 50 == 0 or idx + 1 == iterations:
                print(f'{idx}/{iterations}')
                if self.view_progress:
                    self.visualize()


if __name__ == '__main__':
    layer = Layer()
    layer.train()
    layer.visualize()
