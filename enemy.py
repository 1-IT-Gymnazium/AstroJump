import pygame
from settings import TILE_WIDTH, TILE_HEIGHT


class Projectile:
    def __init__(self, x, y, direction, speed=10):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.image = pygame.image.load("Graphics/laser_bullet/laser_bullet.png")
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        # Move the projectile in the specified direction
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        self.rect.x = self.x - 5
        self.rect.y = self.y + 25

    def draw(self, screen, camera):
        camera_x, camera_y = camera.camera.topleft
        screen.blit(self.image, ((self.x + camera_x) - 5, (self.y + camera_y) + 40))


class ProjectileManager:
    def __init__(self, game):
        self.projectiles = []
        self.last_shot_time = 0
        self.game = game

    def update_projectiles(self, current_time):

        # Update each projectile
        for projectile in self.projectiles:
            projectile.update()

        # Check if it is time to spawn a new projectile
        if current_time - self.last_shot_time >= 2:  # 2 seconds
            self.spawn_projectile()
            self.last_shot_time = current_time

    def spawn_projectile(self):
        for projectile_x, projectile_y in self.game.find_cannons_position(16):
            if projectile_x is not None and projectile_y is not None:
                self.projectiles.append(Projectile(projectile_x * TILE_WIDTH, projectile_y * TILE_HEIGHT, "left"))

    def draw_projectiles(self, screen, camera):
        for projectile in self.projectiles:
            projectile.draw(screen, camera)
            # debugging hit box outline
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(projectile.rect), 1)


class Walker:
    pass
