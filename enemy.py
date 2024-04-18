import pygame
from settings import TILE_WIDTH, TILE_HEIGHT

class Projectile:
    """
    Represents a projectile object in the game which can be fired and moved in a specified direction.

    :param x: Initial x-coordinate of the projectile.
    :param y: Initial y-coordinate of the projectile.
    :param direction: Direction for the projectile to move ('left' or 'right').
    :param speed: Movement speed of the projectile, defaults to 10.
    """
    def __init__(self, x, y, direction, speed=10):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.image = pygame.image.load("Graphics/laser_bullet/laser_bullet.png")
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        """
        Updates the position of the projectile based on its speed and direction.
        """
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        self.rect.x = self.x - 5
        self.rect.y = self.y + 25

    def draw(self, screen, camera):
        """
        Draws the projectile on the screen at its current position adjusted by the camera's top left position.

        :param screen: Pygame surface where the projectile is to be drawn.
        :param camera: Camera object that handles viewport and projection transformations.
        """
        camera_x, camera_y = camera.camera.topleft
        screen.blit(self.image, ((self.x + camera_x) - 5, (self.y + camera_y) + 40))


class ProjectileManager:
    """
    Manages multiple projectiles, their creation, and updating within a game.

    :param game: Reference to the main game object which holds game-wide information and states.
    """
    def __init__(self, game):
        self.projectiles = []
        self.last_shot_time = 0
        self.game = game

    def update_projectiles(self, current_time):
        """
        Updates all managed projectiles and handles the timing for spawning new projectiles.

        :param current_time: Current game time to control projectile spawn timing.
        """
        # Update each projectile
        for projectile in self.projectiles:
            projectile.update()

        # Check if it is time to spawn a new projectile
        if current_time - self.last_shot_time >= 2:  # 2 seconds
            self.spawn_projectile()
            self.last_shot_time = current_time

    def spawn_projectile(self):
        """
        Spawns new projectiles based on the positions of cannons in the game.
        """
        for projectile_x, projectile_y in self.game.find_cannons_position(16):
            if projectile_x is not None and projectile_y is not None:
                self.projectiles.append(Projectile(projectile_x * TILE_WIDTH, projectile_y * TILE_HEIGHT, "left"))

    def draw_projectiles(self, screen, camera):
        """
        Draws all managed projectiles on the screen.

        :param screen: Pygame surface where projectiles are to be drawn.
        :param camera: Camera object to adjust the projectile's drawing position based on the camera's view.
        """
        for projectile in self.projectiles:
            projectile.draw(screen, camera)
            # debugging hit box outline
            # pygame.draw.rect(screen, (255, 0, 0), camera.apply(projectile.rect), 1)
