class Animation :
    def __init__(self, animation_sprites, animation_delay) -> None:
        self.animation_sprites = animation_sprites
        self.animation_delay = animation_delay
        self.time = 0
        self.animation_iterator = 0
    
    def add_time(self, delta_time):
        self.time += delta_time
        if self.time > self.animation_delay:
            self.time = self.time % self.animation_delay
            self.animation_iterator += 1
            self.animation_iterator = self.animation_iterator % len(self.animation_sprites)
    
    def get_sprite(self):
        return self.animation_sprites[self.animation_iterator]

class Animator:
    def __init__(self, animation_dictionary) -> None:
        self.animation_dictionary = animation_dictionary
        self.current_animation = self.animation_dictionary[0]
        self.animated = False

    def set_animation(self, key):
        self.current_animation = self.animation_dictionary[key]

    def stop_animation(self):
        self.animated = False
        self.current_animation.animation_iterator = 0
     
    def start_animation(self):
        self.animated = True

    def get_sprite(self, delta_time):
        if self.animated:
            self.current_animation.add_time(delta_time)
        sprite = self.current_animation.get_sprite()
        return sprite
    