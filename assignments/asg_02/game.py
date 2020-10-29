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


class DrawSection:
    def __init__(self, pos, cell_size, game):
        self.left, self.top = pos
        self.right = self.left + 28 * cell_size
        self.bottom = self.top + 28 * cell_size
        self.img = np.zeros(28 * 28)
        self.game = game
        self.cell_size = cell_size
        self.empty = True
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

    def display_result(self, result):
        self.game.win.blit(self.myfont.render(f'  {result}  ', True, (255, 255, 255), (0, 0, 0)),
                           (self.right + 50, self.top + 50))

    def reset(self, layer):
        if not self.empty:
            self.empty = True
            self.img = np.zeros(28 * 28)
            self.display_result('  -   ')

    def put_pixel(self, screen_pos):
        sx, sy = screen_pos
        x = int((sx - self.left) / self.cell_size)
        y = int((sy - self.top) / self.cell_size)
        if 0 <= x < 28 and 0 <= y < 28:
            self.empty = False
            self.img[y * 28 + x] = 1

    def draw_rect(self):
        pygame.draw.line(self.game.win, (255, 255, 255), (self.left, self.top), (self.left, self.bottom), 5)
        pygame.draw.line(self.game.win, (255, 255, 255), (self.left, self.top), (self.right, self.top), 5)
        pygame.draw.line(self.game.win, (255, 255, 255), (self.right, self.bottom), (self.left, self.bottom), 5)
        pygame.draw.line(self.game.win, (255, 255, 255), (self.right, self.bottom), (self.right, self.top), 5)
        self.game.visualize_image(self.img, (self.left, self.top), 5, COLOR.alpha_map((255, 255, 255)))


class Visualiser:
    def __init__(self, width, height, caption='Default caption'):
        self.quit = False
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.mouse_is_pressed = False
        self.square = DrawSection((200, 200), 5, self)
        self.key_is_pressed = False
        self.layer = None

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
            self.key_is_pressed = event.type == pygame.KEYUP

    def draw(self):
        self.square.draw_rect()

    def update(self):
        if self.mouse_is_pressed:
            x, y = pygame.mouse.get_pos()
            # self.put_pixel(int(x), int(y), (255, 255, 255, 0.5))
            self.square.put_pixel((x, y))
            self.square.put_pixel((x, y + 1))
            self.square.put_pixel((x + 1, y))
            self.square.put_pixel((x + 1, y + 1))
            result = self.layer.get_output(self.square.img).argmax()
            self.square.display_result(result)
        if self.key_is_pressed:
            self.square.reset(self.layer)
        self.draw()
        pygame.display.update()

    def run(self, layer):
        self.layer = layer
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
