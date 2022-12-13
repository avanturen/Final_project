from config import *
import pygame
from random import randint
import numpy as np

def get_range(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def get_direction(x1, y1, x2, y2):
    direction = np.array([x2-x1, y2 - y1])
    return direction / np.linalg.norm(direction)



class Enemy:
    def __init__(self, x, y, v, vision_range) -> None:
        self.x = x
        self.y = y
        self.v = v
        self.vision_range = vision_range
        self.direction = [0,0]

    def draw(self, screen, x, y):
        pygame.draw.rect(screen, RED, (self.x - x - 10 + WIDTH/2, self.y - y - 10 + HEIGHT/2, 100, 100))

    def search_player(self, player):
        if (get_range(self.x, self.y, player.rect.x, player.rect.y) < self.vision_range):
            self.direction = get_direction(self.x, self.y, player.rect.x, player.rect.y)
        else:
            self.direction = [0, 0]
    
    def move(self):
        print(self.x, self.y)
        self.x += self.direction[0] * self.v
        self.y += self.direction[1] * self.v

class Enemy_Controller:
    def __init__(self, screen, spawn_time, enemy_power, player) -> None:
        self.screen = screen
        self.spawn_time = spawn_time
        self.enemy_power = enemy_power
        self.enemies = []
        self.timer = 0
        self.player = player
    
    def add_time(self, delta_time):
        self.timer += delta_time
        if self.timer > self.spawn_time:
            self.timer = self.timer % self.spawn_time
            self.spawn_enemy()
        self.move_enemies()

    def draw_enemy(self, x, y):
        for i in self.enemies:
            i.draw(self.screen, x, y)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.search_player(self.player)
            enemy.move()

    def spawn_enemy(self):   
        self.enemies.append(Enemy(randint(0, 3600), randint(0, 2700), 20, 500))