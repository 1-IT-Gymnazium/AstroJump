import pygame


class Enemy:
    def __init__(self, x, y, health, damage):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class Canon(Enemy):
    pass


class Spike:
    def __init__(self, x, y, width, height, image):
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, camera):
        adjusted_rect = camera.apply(self.rect)
        screen.blit(self.image, adjusted_rect.topleft)


class Walker(Enemy):
    pass
