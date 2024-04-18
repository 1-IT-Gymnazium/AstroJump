import pygame
from settings import PLAYER_SPEED, JUMP_FORCE, GRAVITY, VERTICAL_VELOCITY
from animation import load_images, Animation


class Player:
    """
    Represents a player character in a game with capabilities such as movement,
    jumping, and animation handling based on the state.

    :param x: Initial x-coordinate of the player.
    :param y: Initial y-coordinate of the player.
    :param width: Width of the player.
    :param height: Height of the player.
    :param screen: Pygame screen where the player is to be drawn.
    """

    def __init__(self, x, y, width, height, screen):
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.speed = PLAYER_SPEED
        self.move_left = False
        self.move_right = False
        self.is_jumping = False
        self.can_jump = True
        self.jump_force = JUMP_FORCE
        self.gravity = GRAVITY
        self.vertical_velocity = VERTICAL_VELOCITY
        self.rect = pygame.Rect(x, y, width, height)
        self.facing_right = True
        self.assets = {
            "player_idle": Animation(load_images("Idle"), img_dur=10),
            "player_jump": Animation(load_images("Jump")),
            "player_run": Animation(load_images("Run"), img_dur=4),
        }
        self.current_animation = 'player_idle'
        self.jump_sound = pygame.mixer.Sound("Sounds/jump_sound.mp3")
        self.jump_sound.set_volume(0.2)
        self.position_was_reset = False

    def update_animation(self):
        """
        Updates the player's animation state based on the movement and jumping
        flags.
        """
        if self.is_jumping:
            self.current_animation = "player_jump"
        elif self.move_left or self.move_right:
            self.current_animation = "player_run"
        else:
            self.current_animation = "player_idle"

    def draw(self, camera):
        """
        Draws the player on the screen based on the current animation frame and
        camera view.

        :param camera: Camera object that handles viewport and projection
        transformations.
        """
        current_animation = self.assets[self.current_animation]
        current_animation.update()
        current_frame = current_animation.img()
        if not self.facing_right:
            current_frame = pygame.transform.flip(current_frame, True, False)

        rect = camera.apply(self.rect)
        self.screen.blit(current_frame, rect.topleft)

    def handle_event(self, event):
        """
        Handles player input events to update movement and jumping status.

        :param event: Pygame event to be processed.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.move_left = True
                self.facing_right = False
            if event.key == pygame.K_d:
                self.move_right = True
                self.facing_right = True
            if event.key == pygame.K_SPACE:
                if not self.is_jumping and self.can_jump:
                    self.jump_sound.play()
                    self.is_jumping = True
                    self.can_jump = False
                    self.vertical_velocity = -self.jump_force

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.move_left = False
            if event.key == pygame.K_d:
                self.move_right = False

    def is_moving(self):
        """
        Checks if the player is currently moving or jumping.

        :return: True if the player is moving or jumping, False otherwise.
        """
        return self.move_left or self.move_right or self.is_jumping

    def calculate_new_position(self):
        """
        Calculates the new position of the player based on current movement
        and gravity.

        :return: Tuple (new_x, new_y) representing the new position
        coordinates.
        """
        new_x = self.x
        new_y = self.y

        if self.move_left:
            new_x -= self.speed
        if self.move_right:
            new_x += self.speed

        if self.is_jumping:
            new_y += self.vertical_velocity
            self.vertical_velocity += self.gravity
            if self.vertical_velocity > 0:
                self.is_jumping = False

        return new_x, new_y

    def update_position(self, new_x, new_y):
        """
        Updates the player's position on the screen.

        :param new_x: New x-coordinate.
        :param new_y: New y-coordinate.
        """
        if not self.position_was_reset:
            self.x = new_x
            self.y = new_y
            self.rect = pygame.Rect(new_x, new_y, self.width, self.height)

    def reset_position(self):
        """
        Resets the player's position to the initial coordinates.
        """
        self.x = self.initial_x
        self.y = self.initial_y
        self.vertical_velocity = 0
        self.is_jumping = False
        self.can_jump = True
        self.rect.x = self.x
        self.rect.y = self.y
        self.move_left = False
        self.move_right = False
