import pygame
import numpy as np
import math
import camera
from config import *
import numpy as np

class Object:
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.texture = texture





class Player(pygame.sprite.Sprite):
    def __init__(self, x,y, v, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.v = v

    def draw(self, screen, x, y):
        screen.blit(game.player.image, (x, y))

    def move(self, direction):
        self.rect.x += self.v * direction[0]
        self.rect.y -= self.v * direction[1]






class Game:
    _map = None
    colliders = []
    collider_map = 'collide_map.csv'
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, spawn_time: int, font_style: pygame.font.Font, player) -> None:
        self.screen = screen
        self.clock = clock
        self.spawn_time = spawn_time
        self.font_style = font_style
        self.player = player

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
                
            
            if pygame.Rect.colliderect(collider, player.rect):
                if deltax < player.v:
                    direction[0] = 0
                if deltay < player.v:
                    direction[1] = 0
                
        return direction

    def render_colliders(self):
        for collider in self.colliders:
            pygame.draw.rect(self.screen, RED, collider)

    def get_direction(self, keys):
        direction = np.array([0,0])
        if keys[pygame.K_RIGHT]:
            direction[0] += 1
        if keys[pygame.K_LEFT]:
            direction[0] -= 1
        if keys[pygame.K_DOWN]:
            direction[1] -= 1
        if keys[pygame.K_UP]:
            direction[1] += 1
        
        norm =  np.linalg.norm(direction)
        if norm:
            return direction/norm
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
        x_to_array, x_to_render, y_to_array, y_to_render = camera.edge_handing(game.player.rect.x, game.player.rect.y, map_pixels.shape[0], map_pixels.shape[1])
        keys = pygame.key.get_pressed()
        game.screen.blit(game._map, (0, 0), camera.camera_move(x_to_array, y_to_array))
        game.player.move(game.collision_handing(game.player, game.get_direction(keys)))
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