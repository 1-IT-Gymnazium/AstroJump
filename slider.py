import pygame


class Slider:
    """
    Represents a slider UI component that allows users to select a value by moving a handle within a designated range.

    :param x: The x-coordinate of the top-left corner of the slider.
    :param y: The y-coordinate of the top-left corner of the slider.
    :param w: The width of the slider.
    :param h: The height of the slider.
    :param min_val: The minimum value of the slider.
    :param max_val: The maximum value of the slider.
    :param start_val: The initial value of the slider when first displayed.
    """

    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, w, h)  # The background of the slider
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val  # The current value based on the handle's
        # position
        self.handle_rect = pygame.Rect(x, y, h, h)  # The draggable handle
        self.dragging = False  # Status to check if the handle is being dragged

    def draw(self, screen):
        """
        Draws the slider and its handle on the given screen.

        :param screen: The Pygame surface to draw the slider on.
        """
        pygame.draw.rect(screen, (200, 200, 200), self.rect,
                         border_radius=30)  # Slider background
        pygame.draw.rect(screen, (150, 150, 150), self.handle_rect,
                         border_radius=30)  # Slider handle

    def handle_event(self, event, mx, my):
        """
        Handles mouse events to enable dragging of the slider's handle and updating the value.

        :param event: The event to handle, typically from pygame's event queue.
        :param mx: The x-coordinate of the mouse position.
        :param my: The y-coordinate of the mouse position.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(
                    (mx, my)):  # Check if the mouse is over the handle
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update handle position and calculate the new value
            self.handle_rect.x = max(self.rect.x, min(mx, self.rect.x
                                                      + self.rect.width
                                                      - self.handle_rect.width)
                                     )
            self.value = self.min_val + (self.max_val - self.min_val) * (
                (self.handle_rect.x - self.rect.x) / self.rect.width)
