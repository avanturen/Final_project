import pygame
from config import *

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
                pygame.draw.rect(surface, (100, 100, 75), option_rect)
            surface.blit(option, option_rect)


menu = Menu()
menu.new_option("start", lambda: main.game_start())
menu.new_option("quit", lambda: pygame.quit())

running = True
def show_menu():
    running = True
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
        menu_bg = pygame.image.load("assets/menu2.png")
        screen.blit(menu_bg, (0,0))
        menu.draw(screen, 200, 400, 75)

        pygame.display.flip()
    quit()