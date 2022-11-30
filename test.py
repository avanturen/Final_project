import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    pixels = pygame.surfarray.pixels2d(screen)
    screen.fill((255,0,255))
    for i in range(1200):
        for j in range(900):
            pixels[i][j] = randint(0, 16711935)