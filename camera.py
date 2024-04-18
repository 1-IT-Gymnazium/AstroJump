import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class Camera:
    """
    A Camera object that handles the viewing area in the game, focusing on a
    target entity and
    limiting the camera's movement to the dimensions of the map.

    :param width: The width of the area the camera can scroll over.
    :param height: The height of the area the camera can scroll over.
    """

    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """
        Adjusts the position of an entity relative to the current camera
        position.

        :param entity: The entity whose position will be adjusted for camera
        offset.
        :return: The new position of the entity as adjusted by the camera
        offset.
        """
        return entity.move(self.camera.topleft)

    def update(self, target):
        """
        Updates the camera's position based on the target entity, ensuring the
        target remains
        centered in the view, and constraining the camera to the predefined
        boundaries of the map.

        :param target: The entity the camera should focus on and center in
        the view.
        """
        x = -target.x + int(WINDOW_WIDTH / 2)
        y = -target.y + int(WINDOW_HEIGHT / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - WINDOW_WIDTH), x)  # Right

        self.camera = pygame.Rect(x, y, self.width, self.height)
