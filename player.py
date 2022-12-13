from math import pi, sin, cos
import pygame
from animations import Animation, Animator

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, v, filename):
        pygame.sprite.Sprite.__init__(self)
        self.h = 140
        self.w  = 55
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = pygame.Rect(x - self.w/2, y - self.h/2, self.w, self.h)
        self.v = v
        self.sprites = [((3, 44), (53, 44)), ((122, 40), (195, 40), (15, 180)), ((75, 180), (130, 180), (190, 180)), ((260, 44), (250, 180))]
        self.health = 100
        self.weapons = [Weapon(self, 200, 0.1)]
        Animations = []
        for i in self.sprites:
            Animations.append(Animation(i, 20))
        self.animator = Animator(Animations)
        self.direction = 1

    def take_damage(self, damage):
        self.health -= damage

    def draw(self, screen, x, y):
        match self.direction:
            case 1:
                self.animator.set_animation(1)
            case 2:
                self.animator.set_animation(2)
            case 0:
                self.animator.set_animation(0)
            case 3:
                self.animator.set_animation(3)
        screen.blit(self.image, (x, y), (*self.animator.get_sprite(1), self.w, self.h))
        for weapon in self.weapons:
            pygame.draw.circle(screen, (200, 0, 0), (x + weapon.x + self.w/2, y + weapon.y + self.h/2), 5)
            weapon.move()
            print(weapon.rect.x, weapon.rect.y)

    def move(self, direction):
        self.rect.x += self.v * direction[0]
        self.rect.y -= self.v * direction[1]



class Weapon:
    def __init__(self, player, r, v) -> None:
        self.r = r
        self.v = v
        self.s = 0
        self.x = r
        self.y = 0
        self.player = player
        self.rect = pygame.Rect(player.rect.x + r + player.w/2 - 5, player.rect.y + player.h/2 - 5, 10, 10)

    def move(self):
        self.s += self.v
        self.s = self.s % (2 * pi)
        self.y = sin(self.s) * self.r
        self.x = cos(self.s) * self.r
        self.rect.x = self.player.rect.x + self.x + self.player.w/2 -5
        self.rect.y = self.player.rect.y + self.y + self.player.h/2 -5

    
