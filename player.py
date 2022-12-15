from math import pi, sin, cos
import pygame
from animations import Animation, Animator

"""класс игрока"""
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, v, filename):
        pygame.sprite.Sprite.__init__(self)
        self.h = 140
        self.w  = 55
        self.damage = 10
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = pygame.Rect(x - self.w/2, y - self.h/2, self.w, self.h)
        self.v = v
        self.level = 1
        self.new_level = 0

        self.exp = 0
        self.exp_for_lvlup = 100
        self.sprites = [((10, 3), (65, 3)), ((126, 3), (202, 3), (16, 150)), ((76, 150), (134, 150), (192, 150)), ((17, 293), (83, 293))]
        self.health = 100
        self.max_health = 100
        self.weapons = [Weapon(self, 200, 0.1)]
        self.vampire = 0
        Animations = []
        for i in self.sprites:
            Animations.append(Animation(i, 20))
        self.animator = Animator(Animations)
        self.direction = 1

    """функция получения урона"""
    def take_damage(self, damage):
        self.health -= damage
        self.health = int(self.health)
    
    def heal(self, heal):
        self.health += heal
        self.health = int(self.health)
        if self.health > self.max_health:
            self.health = self.max_health

    """функция получения опыта"""
    def get_exp(self, exp):
        self.exp += exp
        if self.exp >= self.exp_for_lvlup:
            self.exp %= self.exp_for_lvlup
            self.level += 1
            self.exp_for_lvlup *= 1.05
            self.new_level = 1

    """функция рисования персонажа"""
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

    """функция движения персонажа"""
    def move(self, direction):
        self.rect.x += self.v * direction[0]
        self.rect.y -= self.v * direction[1]

    """Добавление нового оружия"""
    def new_weapon(self):
        new_weapon = Weapon(self, self.weapons[0].r, self.weapons[0].v)
        self.weapons.append(new_weapon)
        num = len(self.weapons)
        for i in range(num):
            self.weapons[i].s = self.weapons[0].s + 2 * pi * i / num
    


class Weapon:
    """класс оружия"""
    def __init__(self, player, r, v) -> None:
        self.r = r
        self.v = v
        self.s = 0
        self.x = r
        self.y = 0
        self.player = player
        self.rect = pygame.Rect(player.rect.x + r + player.w/2 - 5, player.rect.y + player.h/2 - 5, 10, 10)

    
    def move(self):
        """движение оружия"""
        self.s += self.v
        self.s = self.s % (2 * pi)
        self.y = sin(self.s) * self.r
        self.x = cos(self.s) * self.r
        self.rect.x = self.player.rect.x + self.x + self.player.w/2 -5
        self.rect.y = self.player.rect.y + self.y + self.player.h/2 -5

    
