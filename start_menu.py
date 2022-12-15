import pygame
from config import *
import main

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font1 = pygame.font.SysFont('arial', 50)
"""функции от сюда перенесеры в main"""

class Menu:
    def __init__(self):
        self.options_bottoms = []
        self.functions = []
        self.current = 0

    def new_option(self, option, function):
        self.options_bottoms.append(font1.render(option, True, RED))
        self.functions.append(function)

    """Меняет выбранную в данный момент опцию в меню"""
    def switch(self, direction):
        self.current = max(0, min(self.current + direction, len(self.options_bottoms) - 1))

    def select(self):
        self.functions[self.current]()

    def draw(self, surface, x, y, distance):
        for i, option in enumerate(self.options_bottoms):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * distance)
            if i == self.current:
                pygame.draw.rect(surface, (100, 100, 75), option_rect)
            surface.blit(option, option_rect)




running = True
"""игровой цикл меню"""
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                menu.switch(-1)
            elif e.key == pygame.K_s:
                menu.switch(1)
            elif e.key == pygame.K_SPACE:
                menu.select()
    menu_bg = pygame.image.load("assets/menubg.png")
    screen.blit(menu_bg, (0,0))
    menu.draw(screen, 100, 100, 75)

    pygame.display.flip()
quit()
