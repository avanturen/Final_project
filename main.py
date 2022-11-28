import pygame
import numpy as np
import math
from config import *


class Collider:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

class Object:
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.texture = texture





class Player(Object):
    def __init__(self, x, y, v, texture):
        super().__init__(x, y, texture)
        self.v = v

    def move(self, direction):
        self.x += self.v * direction[0]
        self.y -= self.v * direction[1]

    def render(self, screen):
        #FIX
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 20)
    




class Game:

    colliders = []
    collider_map = 'collide_map.csv'
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, spawn_time: int, font_style: pygame.font.Font, player) -> None:
        self.screen = screen
        self.clock = clock
        self.spawn_time = spawn_time
        self.font_style = font_style
        self.player = player
    def start(self) -> None:
        """Game start"""
        self.parse_colliders()
        finished = False
        while not finished:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
            keys = pygame.key.get_pressed()

            self.player.move(self.collision_handing(self.player, self.get_direction(keys)))
            self.player.render(self.screen)
            self.render_colliders()
            pygame.display.update()

            self.screen.fill(BLACK)


    def parse_colliders(self):
        with open(self.collider_map) as f:
            for line in f.readlines():
                line = list(map(int, line.split()))
                self.colliders.append(Collider(line[0], line[1], line[2], line[3]))

    


    def collision_handing(self, player, direction):
        playerx = player.x + direction[0] * player.v
        playery = player.y - direction[1] * player.v
        for collider in self.colliders:
            deltax1 = playerx - collider.x1
            deltax2 = collider.x2 - playerx
            deltay1 = playery - collider.y1
            deltay2 = collider.y2 - playery
            if (deltax1 * deltax2 >= 0) and (deltay1 * deltay2 >= 0):
                if (deltax1 < player.v ) or (deltax2 < player.v):
                    direction[0] = 0
                if (deltay1 < player.v) or (deltay2 < player.v):
                    direction[1] = 0
                
        return direction


    def render_colliders(self):
        for collider in self.colliders:
            pygame.draw.rect(self.screen, RED, (collider.x1, collider.y1, collider.x2 - collider.x1, collider.y2 - collider.y1))

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



def main():
    """Main function"""
    screen, font_style, clock = init()
    player = Player(500, 500, 5, 50)
    game = Game(screen, clock, 500, font_style, player)
    game.start()
    pygame.quit()


if __name__ == '__main__':
    main()