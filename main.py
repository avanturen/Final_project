import pygame
import client
import json
import config
from game_classes import *
import random

class Game:
    def __init__(self, screen, clock, FPS, name, WIDTH, HEIGHT) -> None:
        self.screen = screen
        self.clock = clock
        self.FPS = FPS
        self.name = name
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
    
    def start(self):
        char = Character(name, random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT))
        characters = [char]
        finished = False
        while not finished:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_LEFT]:
                char.x -= 3
            if keys[pygame.K_RIGHT]:
                char.x += 3
            if keys[pygame.K_DOWN]:
                char.y += 3
            if keys[pygame.K_UP]:
                char.y -= 3
            characters = json.loads(client.send_message(char.get_json()))
            for character in characters:
                pygame.draw.circle(screen, (180, 180, 180), (character['x'], character['y']), 5)
            pygame.display.update()
            screen.fill((0,0,0))


if __name__ == '__main__':
    pygame.init()
    name = input()
    FPS = 30
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    game = Game(screen, clock, FPS, name, config.WIDTH, config.HEIGHT)
    game.start()
    pygame.quit()