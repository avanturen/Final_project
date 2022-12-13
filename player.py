import pygame
from animations import Animation, Animator

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, v, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = pygame.Rect(x - 45, y - 140, 110, 280)
        self.v = v
        self.sprites = [((5, 10), (105, 10)), ((240, 10), (400, 10), (35, 300)), ((160, 300), (265, 300), (380, 300)), ((530, 10), (510, 300))]
        Animations = []
        for i in self.sprites:
            Animations.append(Animation(i, 20))
        self.animator = Animator(Animations)
        self.direction = 1

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
        screen.blit(self.image, (x, y), (*self.animator.get_sprite(1), 110, 280))

    def move(self, direction):
        self.rect.x += self.v * direction[0]
        self.rect.y -= self.v * direction[1]