import pygame
from settings import TILE_WIDTH, TILE_HEIGHT, WINDOW_WIDTH


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

    def draw(self, screen, camera):
        pass


class Projectile:
    def __init__(self, x, y, direction, speed=10):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))

    def update(self):
        # Move the projectile in the specified direction
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed

    def draw(self, screen, camera):
        camera_x, camera_y = camera.camera.topleft
        screen.blit(self.image, (self.x + camera_x, self.y + camera_y))


class ProjectileManager:
    def __init__(self, game):
        self.projectiles = []
        self.last_shot_time = 0
        self.game = game  # Reference to the Game instance to access shared resources

    def update_projectiles(self, current_time):
        # Remove off-screen projectiles
        self.projectiles = [proj for proj in self.projectiles if 0 < proj.x < WINDOW_WIDTH]

        # Update each projectile
        for projectile in self.projectiles:
            projectile.update()

        # Check if it is time to spawn a new projectile
        if current_time - self.last_shot_time >= 2:  # 2 seconds
            self.spawn_projectile()
            self.last_shot_time = current_time

    def spawn_projectile(self):
        tile_x, tile_y = self.game.find_tile_position(16)
        if tile_x is not None and tile_y is not None:
            self.projectiles.append(Projectile(tile_x * TILE_WIDTH, tile_y * TILE_HEIGHT, "left"))

    def draw_projectiles(self, screen, camera):
        for projectile in self.projectiles:
            projectile.draw(screen, camera)


class Walker(Enemy):
    pass
