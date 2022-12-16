from math import atan2, pi, sqrt, sin, cos

import pygame
import numpy as np

from config import *
from random import randint, random
from animations import Animation, Animator

"""Анимации врагов"""


def get_range(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def get_direction(x1, y1, x2, y2):
    direction = np.array([x2 - x1, y2 - y1])
    return direction / np.linalg.norm(direction)


def get_animation(filenames):
    animations = []
    for filename in filenames:
        animations.append(pygame.transform.scale2x(pygame.image.load(filename).convert_alpha()))
    return Animation(animations, 20)


class Enemy:
    def __init__(self, x, y, v, vision_range, health) -> None:
        self.type = randint(0, 2)
        self.v = v / (self.type + 4) * 4
        self.animator = Animator([get_animation(PATH[self.type])])
        self.vision_range = vision_range
        self.health = health * sqrt(self.type + 1)
        self.direction = [(random() - 1) / 200, (random() - 1) / 200]
        self.rect = pygame.Rect(x - 25, y - 25, 50, 50)
        self.rect_to_draw = pygame.Rect(self.rect.x - 25, self.rect.y - 25, 50, 50)
        self.visible = False

    def draw(self, screen, x, y):
        """Отрисовка врага"""
        if self.visible:
            image = pygame.transform.rotate(self.animator.get_sprite(1),
                                            -atan2(self.direction[1], self.direction[0]) * 180 / pi)
            self.rect = image.get_rect(center=self.rect.center)
            self.rect_to_draw = image.get_rect(center=self.rect.center)
            self.rect_to_draw.x = self.rect.x - x - 10 + WIDTH / 2
            self.rect_to_draw.y = self.rect.y - y - 10 + HEIGHT / 2
            screen.blit(image, (self.rect_to_draw.x, self.rect_to_draw.y))

    def is_in_wall(self, walls):
        """Проверка, в стене ли враг"""
        collide = pygame.rect.Rect.collidelist(self.rect, walls)
        if (collide < 0) or (collide > 14):
            self.visible = True
        else:
            self.visible = False

    def get_damage(self, damage):
        """Функция, наносящая врагу урон"""
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    def search_player(self, player):
        """функция, которая ориентирует движение врагов в направлении игрока"""
        self.direction = get_direction(self.rect.x, self.rect.y, player.rect.x + player.w / 2,
                                       player.rect.y + player.h / 2)
        self.animator.start_animation()

    def move(self):
        """движение врага"""
        self.rect.x += self.direction[0] * self.v
        self.rect.y += self.direction[1] * self.v


class EnemyController:
    def __init__(self, screen, spawn_time, enemy_power, player, power_up_time) -> None:
        self.screen = screen
        self.max_enemies = 10
        self.spawn_time = spawn_time
        self.enemy_power = enemy_power
        self.power_up_time = power_up_time
        self.power_up_timer = 0
        self.enemies = {}
        self.damage_reduce = 1
        self.exp_for_enemy = enemy_power * 3
        self.enemy_counter = 0
        self.timer = 0
        self.player = player

    def wall_handler(self, walls):
        """Проверка, видно ли врагов"""
        for enemy in self.enemies.values():
            enemy.is_in_wall(walls)

    def add_time(self, delta_time):
        """Добавляет время к игровому таймеру"""
        self.timer += delta_time
        self.power_up_timer += delta_time
        if self.timer > self.spawn_time:
            self.timer = self.timer % self.spawn_time
            self.spawn_enemy()
        if self.power_up_timer > self.power_up_time:
            self.power_up_timer %= self.power_up_time
            self.enemy_power *= 1.03
            self.max_enemies = int(self.max_enemies * 1.05)
        self.move_enemies()

    def is_atack(self):
        """Проверка, атакует ли враг игрока"""
        to_delete = []
        for (i, enemy) in self.enemies.items():
            if pygame.Rect.colliderect(enemy.rect, self.player.rect):
                self.player.take_damage(self.enemy_power * sqrt(enemy.type + 1) * self.damage_reduce)
                to_delete.append(i)
        for i in to_delete:
            self.enemies.pop(i)

    def is_atacked(self):
        """Функция, проверяющая, атакован ли враг, и в зависимости от результата наносящая ему урон"""
        to_delete = []
        exp = 0
        for (i, enemy) in self.enemies.items():
            for orbit in self.player.orbits:
                for weapon in orbit.weapons:
                    if pygame.Rect.colliderect(enemy.rect, weapon.rect):
                        self.player.heal(self.player.vampire * self.player.damage)
                        if enemy.get_damage(orbit.damage):
                            to_delete.append(i)
                            self.player.get_exp(self.exp_for_enemy * sqrt(1 + enemy.type))
                            exp += int(self.exp_for_enemy * sqrt(1 + enemy.type))
                            self.player.heal(orbit.damage * orbit.vampire * 2)
        to_delete = set(to_delete)
        for i in to_delete:
            self.enemies.pop(i)
        self.spawn_enemy()
        return exp

    def draw_enemy(self, x, y):
        """Отрирсовка врагов"""
        for i in self.enemies.values():
            i.draw(self.screen, x, y)

    def move_enemies(self):
        """Движение врагов"""
        for enemy in self.enemies.values():
            enemy.search_player(self.player)
            enemy.move()

    def spawn_enemy(self):
        """Появление врагов"""
        for i in range(self.max_enemies - len(self.enemies)):
            r = random() * 1000 + 400
            angle = random() * 2 * pi
            self.enemies[self.enemy_counter] = Enemy(self.player.rect.x + r * cos(angle),
                                                     self.player.rect.y + r * sin(angle), 4, 500,
                                                     60 * self.enemy_power / 10)
            self.enemy_counter += 1
