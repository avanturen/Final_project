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
    def __init__(self, x, y, v, vision_range, health) -> None:
        self.v = v
        self.vision_range = vision_range
        self.health = health
        self.direction = [0,0]
        self.rect = pygame.Rect(x - 25, y - 25, 50, 50)
        self.rect_to_draw = pygame.Rect(self.rect.x -25, self.rect.y - 25, 50, 50)

    def draw(self, screen, x, y):
        self.rect_to_draw.x = self.rect.x - x - 10 + WIDTH/2
        self.rect_to_draw.y = self.rect.y - y - 10 + HEIGHT/2
        pygame.draw.rect(screen, RED, self.rect_to_draw)


    def get_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    def search_player(self, player):
        if (get_range(self.rect.x, self.rect.y, player.rect.x + player.w/2, player.rect.y + player.h/2) < self.vision_range):
            self.direction = get_direction(self.rect.x, self.rect.y, player.rect.x + player.w/2, player.rect.y + player.h/2)
        else:
            self.direction = [0, 0]
    
    def move(self):
        
        self.rect.x += self.direction[0] * self.v
        self.rect.y += self.direction[1] * self.v

class Enemy_Controller:
    def __init__(self, screen, spawn_time, enemy_power, player, power_up_time) -> None:
        self.screen = screen
        self.spawn_time = spawn_time
        self.enemy_power = enemy_power
        self.power_up_time = power_up_time
        self.power_up_timer = 0
        self.enemies = {}
        self.exp_for_enemy = enemy_power * 10
        self.enemy_counter = 0
        self.timer = 0
        self.player = player
    
    def add_time(self, delta_time):
        self.timer += delta_time
        self.power_up_timer += delta_time
        if self.timer > self.spawn_time:
            self.timer = self.timer % self.spawn_time
            self.spawn_enemy()
        if self.power_up_timer > self.power_up_time:
            self.power_up_timer %= self.power_up_time
            self.enemy_power *= 1.1
        self.move_enemies()

    def is_atack(self):
        to_delete = []
        for (i, enemy) in self.enemies.items():
            if pygame.Rect.colliderect(enemy.rect, self.player.rect):
                self.player.take_damage(self.enemy_power)
                to_delete.append(i)
        for i in to_delete:
            self.enemies.pop(i)

    def is_atacked(self):
        to_delete = []
        for (i, enemy) in self.enemies.items():
            for weapon in self.player.weapons:
                if pygame.Rect.colliderect(enemy.rect, weapon.rect):
                    if enemy.get_damage(self.player.damage):
                        to_delete.append(i)
                        self.player.get_exp(self.exp_for_enemy)
                    print(self.player.level)
        for i in to_delete:
            self.enemies.pop(i)
    def draw_enemy(self, x, y):
        for i in self.enemies.values():
            i.draw(self.screen, x, y)

    def move_enemies(self):
        for enemy in self.enemies.values():
            enemy.search_player(self.player)
            enemy.move()

    def spawn_enemy(self):   
        self.enemies[self.enemy_counter] = Enemy(randint(0, 3600), randint(0, 2700), self.enemy_power/2, 500, 6*self.enemy_power)
        self.enemy_counter += 1