import pygame
from random import choice, randint as rnd
import math
import camera
from config import *
import numpy as np


class Object:
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.texture = texture


class Target:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = rnd(0, 2700)
        self.y = rnd(0, 3600)
        self.r = 50
        self.color = RED

        self.flag = 1

    def new_target(self):
        """создание цели"""
        self.x = rnd(0, 2700)
        self.y = rnd(0, 3600)
        self.r = 50
        self.live = 1
        self.flag = 1

    def loot(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self, screen, x, y, r):
        pygame.draw.circle(screen, self.color, x, y, r)



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, v, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = pygame.Rect(x - 45, y - 140, 110, 280)
        self.v = v
        self.sprites = [((5, 10), (105, 10)), ((240, 10), (400, 10), (35, 300)), ((160, 300), (265, 300), (380, 300)),
                        ((530, 10), (510, 300))]
        self.in_motion = True
        self.direction = 1
        self.animation_tik = 0

    def draw(self, screen, x, y):
        if self.in_motion:
            self.animation_tik += 0.05
        match self.direction:
            case 1:
                to_draw = 1
            case 2:
                to_draw = 2
            case 0:
                to_draw = 0
            case 3:
                to_draw = 3
        screen.blit(self.image, (x, y),
                    (*self.sprites[to_draw][int(self.animation_tik) % len(self.sprites[to_draw])], 110, 280))

    def move(self, direction):
        self.rect.x += self.v * direction[0]
        self.rect.y -= self.v * direction[1]
<<<<<<< HEAD
=======




>>>>>>> parent of 5397e84 (НОВАЯ ИГРА)


class Game:
    _map = None
    colliders = []
    collider_map = 'collide_map.csv'
<<<<<<< HEAD

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, spawn_time: int, font_style: pygame.font.Font,
                 player) -> None:
=======
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, spawn_time: int, font_style: pygame.font.Font, player) -> None:
>>>>>>> parent of 5397e84 (НОВАЯ ИГРА)
        self.screen = screen
        self.clock = clock
        self.spawn_time = spawn_time
        self.font_style = font_style
        self.player = player
        self.target = Target(screen)

    def parse_colliders(self):
        with open(self.collider_map) as f:
            for line in f.readlines():
                line = list(map(int, line.split()))
                self.colliders.append(pygame.Rect((line[0], line[1], line[2] - line[0], line[3] - line[1])))

    def collision_handing(self, player, direction):
        for collider in self.colliders:
            if direction[0] > 0:
                deltax = player.rect.right - collider.left - direction[0] * player.v
            else:
                deltax = collider.right - player.rect.left + direction[0] * player.v
            if direction[1] > 0:
                deltay = collider.bottom - player.rect.top - direction[1] * player.v
            else:
                deltay = player.rect.bottom + direction[1] * player.v - collider.top
<<<<<<< HEAD

=======
                
            
>>>>>>> parent of 5397e84 (НОВАЯ ИГРА)
            if pygame.Rect.colliderect(collider, player.rect):
                if deltax < player.v:
                    direction[0] = 0
                if deltay < player.v:
                    direction[1] = 0

        return direction

    def render_colliders(self):
        for collider in self.colliders:
            pygame.draw.rect(self.screen, RED, collider)

    def get_direction(self, keys, player):
        direction = np.array([0, 0])
        if keys[pygame.K_DOWN]:
            direction[1] -= 1
            player.direction = 1
        elif keys[pygame.K_UP]:
            direction[1] += 1
            player.direction = 2
        if keys[pygame.K_RIGHT]:
            direction[0] += 1
            player.direction = 0
        elif keys[pygame.K_LEFT]:
            direction[0] -= 1
            player.direction = 3

        norm = np.linalg.norm(direction)
        if norm:
            player.in_motion = True
            return direction / norm
        player.in_motion = False
        return direction


def init():
    """Initialize game"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font_style = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    return (screen, font_style, clock)


def loop(game):
    game._map = pygame.image.load('assets/1level.png').convert_alpha()
    map_pixels = pygame.surfarray.array2d(game._map)
    game.parse_colliders()
    finished = False
    while not finished:
        game.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        x_to_array, x_to_render, y_to_array, y_to_render = camera.edge_handing(game.player.rect.x, game.player.rect.y,
                                                                               map_pixels.shape[0], map_pixels.shape[1])
        keys = pygame.key.get_pressed()
        game.screen.blit(game._map, (0, 0), camera.camera_move(x_to_array, y_to_array))
        game.player.move(game.collision_handing(game.player, game.get_direction(keys, game.player)))
        game.player.draw(game.screen, x_to_render, y_to_render)

        pygame.display.update()

    pygame.quit()


def start():
    screen, font_style, clock = init()
    player = Player(900, 700, 10, 'assets/player.png')
    game = Game(screen, clock, 500, font_style, player)
    return game


if __name__ == '__main__':
    game = start()
    loop(game)
