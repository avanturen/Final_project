import pygame
from config import *
from pygame import *
import main

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font1 = pygame.font.SysFont('arial', 50)


class Menu:
    def __init__(self):
        self.options_bottoms = []
        self.functions = []
        self.current = 0

    def new_option(self, option, function):
        self.options_bottoms.append(font1.render(option, True, RED))
        self.functions.append(function)

    def switch(self, direction):
        self.current = max(0, min(self.current + direction, len(self.options_bottoms) - 1))

    def select(self):
        self.functions[self.current]()

    def draw(self, surface, x, y, distance):
        for i, option in enumerate(self.options_bottoms):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * distance)
            if i == self.current:
                draw.rect(surface, (100, 100, 75), option_rect)
            surface.blit(option, option_rect)


menu = Menu()
menu.new_option("start", lambda: main.game_start())
menu.new_option("quit", lambda: pygame.quit())

running = True

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                menu.switch(-1)
            elif e.key == K_s:
                menu.switch(1)
            elif e.key == K_SPACE:
                menu.select()

    screen.fill((0, 0, 0))
    menu.draw(screen, 100, 100, 75)

    display.flip()
quit()
