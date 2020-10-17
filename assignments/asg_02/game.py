import pygame
import sys
from main import get_stuff

pygame.init()

W = 28
H = 28
size = 5
win = pygame.display.set_mode((W * size, H * size))
pygame.display.set_caption('RN')
quit_game = False
left_is_pressed = False


train_set, valid_set, test_set = get_stuff()
idx = 0





def put_gray_scale(x, y, value):
    assert 0 <= value <= 1
    scale = 255 * value
    # scale = 255 if value else 0
    put_pixel(x, y, (scale, scale, 0))


def put_pixel(x, y, color=(255, 255, 255)):
    pygame.draw.rect(win, color, (x * size, y * size, size, size))


def print_img(img):
    for i, pixel in enumerate(img):
        x = i % W
        y = int(i / H)
        put_gray_scale(x, y, pixel)


print('press SPACE')
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            quit_game = True
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            left_is_pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            left_is_pressed = False

        if left_is_pressed:
            x, y = pygame.mouse.get_pos()
            x = int(x / size)
            y = int(y / size)
            put_gray_scale(x,y,1)

        if event.type == pygame.KEYDOWN:
            images, results = train_set
            img, res = images[idx], results[idx]
            idx += 1
            print_img(img)
            print(res)

    pygame.display.update()
