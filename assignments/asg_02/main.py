import pickle
import gzip
import numpy as np
import os
from game import Visualiser, COLOR, pygame
import uuid


class LayerRendering:
    def __init__(self):
        pygame.init()
        self.size_on_screen = 4
        self.game = Visualiser(28 * self.size_on_screen * 10, 28 * self.size_on_screen)


class Layer:
    def __init__(self, view_progress):
        self.control = None
        self.weights = np.zeros([28 * 28, 10])
        self.bias = np.zeros(10)
        self.delta = 0.7
        self.best_accuracy = 0
        self._render = None
        self.view_progress = view_progress
        path = os.path.join('data', 'mnist.pkl.gz')
        with gzip.open(path, 'rb') as f:
            self.train_set, self.valid_set, self.test_set = pickle.load(f, encoding='latin')

    @property
    def render(self):
        if not self._render:
            self._render = LayerRendering()
        return self._render

    def visualize(self):
        # self.render.game.visualize_image(img, (0, 0), self.size_on_screen, COLOR.alpha_map((255, 255, 255)))
        threshold = 10
        for perceptron in range(10):
            self.render.game.visualize_image(self.weights[:, perceptron],
                                             (28 * self.render.size_on_screen * perceptron, 0),
                                             self.render.size_on_screen, COLOR.weight_map(threshold))
        self.render.game.update()

    def change_delta(self, accuracy):
        self.delta = self.delta = (1 - accuracy) ** 4
        self.delta *= 1.3

        print(self.delta)

    def serialize(self, accuracy):
        filename = f'{int(accuracy * 10000)}-{uuid.uuid4()}.p'
        filepath = os.path.join('cache', filename)
        with open(filepath, 'wb') as fd:
            pickle.dump((self.weights, self.bias), fd)

    def load_best_from_cache(self):
        best_file = max(os.listdir('cache'), key=lambda x: int(x.split('-')[0]))
        accuracy = float(best_file.split("-")[0]) / 10000
        with open(os.path.join('cache', best_file), 'rb') as fd:
            self.weights, self.bias = pickle.load(fd)
            self.change_delta(accuracy)
            self.best_accuracy = accuracy
            print(f'Loaded weights and bias from cache with accuracy = {accuracy * 100}%')

    def get_output(self, img):
        return np.dot(img, self.weights) + self.bias

    def train_with_set(self, training_set):
        images, results = training_set
        dataset = list(zip(images, results))
        np.random.shuffle(dataset)
        for img, result in dataset:
            x = img
            z = self.get_output(x)

            # z is a 1d array of length 10, loops wont affect performance
            output = np.array([1 if i > 0 else 0 for i in z])

            t = np.zeros(10)
            t[result] = 1

            x = np.broadcast_to(np.reshape(x, (len(x), 1)), (28 * 28, len(output)))

            self.weights = self.weights + x * (t - output) * self.delta
            self.bias = self.bias + (t - output) * self.delta

    def test_img(self, img, result):
        return self.get_output(img).argmax() == result

    def get_accuracy(self, dataset):
        images, results = dataset
        total_cases = len(images)
        valid_cases = sum(self.test_img(img, result) for img, result in zip(images, results))
        return valid_cases / total_cases

    def train(self, iterations):
        tests = [self.best_accuracy]
        for idx in range(iterations):
            self.train_with_set(self.train_set)
            accuracy = self.get_accuracy(self.valid_set)
            if accuracy > self.best_accuracy:
                self.best_accuracy = accuracy
                self.serialize(accuracy)
            tests.append(accuracy)
            self.change_delta(accuracy)
            print(f'iteration {idx + 1}/{iterations}: {accuracy * 100}%  -  best: {max(tests) * 100}%')
            if accuracy == 1:
                break
        return tests


layer = Layer(view_progress=True)
layer.load_best_from_cache()
# layer.train(iterations=500)
print(layer.get_accuracy(layer.test_set))
layer.visualize()
# layer.render.game.run()  # this allows pygame event loop to run
