import pygame
import sys
import numpy as np



class COLOR:
    @staticmethod
    def rgb(r, g, b):
        return r, g, b

    @staticmethod
    def rgba(r, g, b, a):
        assert 0 <= a <= 1
        return r * a, g * a, b * a

    @staticmethod
    def weight_map(threshold):
        def func(weight):
            value = min(abs(weight), threshold) / threshold * 255
            if weight > 0:
                return 0, value, 0
            else:
                return value, 0, 0

        return func

    @staticmethod
    def alpha_map(color):
        r, g, b = color

        def func(alpha):
            return COLOR.rgba(r, g, b, alpha)

        return func


class Visualiser:
    def __init__(self, width, height, caption='Default caption'):
        self.quit = False
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

        self.mouse_is_pressed = False

    def put_pixel(self, x, y, color):
        pygame.draw.rect(self.win, color, (x, y, 1, 1))

    def draw_rect(self, color, rect):
        pygame.draw.rect(self.win, color, rect)

    def collect_meta_data(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.quit = True
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_is_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_is_pressed = False

    def update(self):
        if self.mouse_is_pressed:
            x, y = pygame.mouse.get_pos()
            self.put_pixel(int(x), int(y), (255, 255, 255, 0.5))
        pygame.display.update()

    def run(self):
        while not self.quit:
            self.collect_meta_data()
            self.update()

    def visualize_image(self, input_img, pos, cell_size, map_color):
        x, y = pos
        width, height = 28, 28
        assert len(input_img) == width * height, \
            f'Invalid dimensions {len(input_img)} != {width} x {height}'
        for i, value in enumerate(input_img):
            dx = i % width
            dy = int(i / height)
            color = map_color(value)
            left = x + dx * cell_size
            top = y + dy * cell_size
            self.draw_rect(color, (left, top, cell_size, cell_size))
