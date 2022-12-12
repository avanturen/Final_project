import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))

class A(pygame.sprite.Sprite):
    def __init__(self, screen) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/map.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = ( 600, 450)
        self.screen = screen
    def draw(self):
        self.screen.blit(self.image, self.rect)

    def rot_center(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    a = A(screen)
    a.draw()
    a.rot_center(1)
    a.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        
        
    pygame.display.update()
    
    